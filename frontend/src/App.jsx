import React, { useState, useEffect, useRef } from 'react';
import { Search, Activity, Terminal, ShieldAlert, CheckCircle, HelpCircle, XCircle, ArrowRight, RefreshCw } from 'lucide-react';

export default function App() {
  const [symbol, setSymbol] = useState('');
  const [loading, setLoading] = useState(false);
  const [streamLogs, setStreamLogs] = useState([]);
  const [activeTab, setActiveTab] = useState('verdict'); // verdict, data
  const [jobState, setJobState] = useState({
    status: 'idle',
    gatheredData: null,
    verdict: null
  });

  const consoleEndRef = useRef(null);
  const eventSourceRef = useRef(null);

  // Auto-scroll streaming console natively
  useEffect(() => {
    if (consoleEndRef.current) {
      consoleEndRef.current.scrollIntoView({ behavior: 'smooth' });
    }
  }, [streamLogs]);

  // Clean up residual SSE pipelines on unmount
  useEffect(() => {
    return () => {
      if (eventSourceRef.current) {
        eventSourceRef.current.close();
      }
    };
  }, []);

  const startResearchStream = async (e) => {
    e.preventDefault();
    const cleanSymbol = symbol.trim().toUpperCase();
    if (!cleanSymbol) return;

    // Reset interface workspace states
    setLoading(true);
    setStreamLogs([{ time: new Date().toLocaleTimeString(), type: 'status', content: `Connecting testing console pipeline for ticker: ${cleanSymbol}...` }]);
    setJobState({ status: 'pending', gatheredData: null, verdict: null });
    setActiveTab('verdict');

    if (eventSourceRef.current) {
      eventSourceRef.current.close();
    }

    try {
      // 1. Submit tracking job initializer row
      const res = await fetch(`http://localhost:8000/api/research`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ symbol: cleanSymbol })
      });

      if (!res.ok) {
        const errData = await res.json().catch(() => ({}));
        throw new Error(errData.detail || 'Failed to initialize backend job tracker.');
      }

      // 2. Open live Server-Sent Events monitoring listener stream
      const streamUrl = `http://localhost:8000/api/research/${cleanSymbol}/stream`;
      const es = new EventSource(streamUrl);
      eventSourceRef.current = es;

      es.onmessage = (event) => {
        try {
          // Check if payload contains raw JSON strings prefixed to data channel
          let chunkStr = event.data;
          if (chunkStr.startsWith("data: ")) {
            chunkStr = chunkStr.substring(6);
          }
          
          const payload = JSON.parse(chunkStr);
          const timestamp = new Date().toLocaleTimeString();

          // Intercept finished Phase 2 final verdict strings
          if (payload.type === 'verdict') {
            try {
              const parsedVerdict = typeof payload.content === 'string' ? JSON.parse(payload.content) : payload.content;
              setJobState(prev => ({ ...prev, status: 'completed', verdict: parsedVerdict }));
            } catch (err) {
              setJobState(prev => ({ ...prev, status: 'completed', verdict: { raw: payload.content } }));
            }
            setLoading(false);
            es.close();
          } else if (payload.type === 'status' && payload.content.includes('fully complete')) {
            setLoading(false);
            es.close();
            // Fetch final consolidated state records explicitly to refresh extracted parameter strings cleanly
            fetchStateExplicitly(cleanSymbol);
          } else if (payload.type === 'error') {
            setLoading(false);
            es.close();
            setJobState(prev => ({ ...prev, status: 'failed' }));
          }

          setStreamLogs(prev => [...prev, { time: timestamp, type: payload.type, content: payload.content }]);
        } catch (e) {
          // Render plain fallback block text rows cleanly
          setStreamLogs(prev => [...prev, { time: new Date().toLocaleTimeString(), type: 'thought', content: event.data }]);
        }
      };

      es.onerror = () => {
        setStreamLogs(prev => [...prev, { time: new Date().toLocaleTimeString(), type: 'error', content: 'SSE transport pipeline interlock closed.' }]);
        setLoading(false);
        es.close();
        // Fallback fetch final generated DB profiles dynamically
        fetchStateExplicitly(cleanSymbol);
      };

    } catch (err) {
      setStreamLogs(prev => [...prev, { time: new Date().toLocaleTimeString(), type: 'error', content: `Exception: ${err.message}` }]);
      setLoading(false);
      setJobState(prev => ({ ...prev, status: 'failed' }));
    }
  };

  const fetchStateExplicitly = async (targetSymbol) => {
    try {
      const res = await fetch(`http://localhost:8000/api/research/${targetSymbol}`);
      if (res.ok) {
        const data = await res.json();
        setJobState(prev => ({
          ...prev,
          status: data.status,
          gatheredData: data.gathered_data,
          verdict: data.verdict ? (data.verdict.scores ? data.verdict : prev.verdict) : prev.verdict
        }));
      }
    } catch (e) {
      // Ignore background refresh errors quietly
    }
  };

  // Helper visual indicator mapping verdict badge containers
  const renderVerdictBadge = (verdictStr) => {
    const cleanStr = (verdictStr || 'WAIT').toUpperCase();
    let badgeClass = 'badge-wait';
    if (cleanStr.includes('BUY')) badgeClass = 'badge-buy';
    else if (cleanStr.includes('HOLD')) badgeClass = 'badge-hold';
    else if (cleanStr.includes('SKIP') || cleanStr.includes('FAIL')) badgeClass = 'badge-skip';
    
    return <div className={`verdict-badge ${badgeClass}`}>{cleanStr}</div>;
  };

  // Helper matrix mapper rendering status marker cells
  const renderStatusIcon = (statusStr) => {
    const s = (statusStr || '').trim();
    if (s === '✓' || s.toLowerCase() === 'pass') return <span className="status-cell status-pass">✓ PASS</span>;
    if (s === '✗' || s.toLowerCase() === 'fail') return <span className="status-cell status-fail">✗ FAIL</span>;
    return <span className="status-cell status-marginal">≈ MARGINAL</span>;
  };

  return (
    <div className="app-container">
      <header>
        <div className="logo-container">
          <div className="logo-icon">
            <Activity color="#ffffff" size={22} />
          </div>
          <span className="app-title">Stock Deep Research Console</span>
        </div>
        <div>
          <span style={{ fontSize: '0.85rem', color: 'var(--text-muted)', fontWeight: 600 }}>
            LM Studio Agentic Runtime Interface
          </span>
        </div>
      </header>

      <form onSubmit={startResearchStream} className="controls-grid">
        <div className="input-wrapper">
          <input
            type="text"
            className="symbol-input"
            placeholder="ENTER STOCK SYMBOL (e.g., SUNPHARMA, INFOTECH, TCS)"
            value={symbol}
            onChange={(e) => setSymbol(e.target.value)}
            disabled={loading}
          />
          <Search style={{ position: 'absolute', right: '1rem', color: 'var(--text-muted)' }} size={20} />
        </div>
        <button type="submit" className="btn-primary" disabled={loading || !symbol.trim()}>
          {loading ? (
            <>
              <RefreshCw className="spinning" size={18} />
              <span>RESEARCHING...</span>
            </>
          ) : (
            <>
              <span>LAUNCH DEEP RUN</span>
              <ArrowRight size={18} />
            </>
          )}
        </button>
      </form>

      <main className="dashboard-grid">
        {/* Left Side: Dynamic Real-time SSE Terminal Streamer */}
        <section className="glass-panel stream-console">
          <div className="console-header">
            <div className="console-title">
              <Terminal size={16} color="var(--accent-color)" />
              <span>LIVE AUTONOMOUS EXECUTION LOGS</span>
            </div>
            <div className="terminal-dots">
              <div className="dot dot-red"></div>
              <div className="dot dot-yellow"></div>
              <div className="dot dot-green"></div>
            </div>
          </div>
          <div className="console-body">
            {streamLogs.length === 0 ? (
              <div style={{ color: 'var(--text-muted)', fontStyle: 'italic', marginTop: '1rem' }}>
                Awaiting ticker target entry to trigger secure local browser contexts...
              </div>
            ) : (
              streamLogs.map((log, idx) => (
                <div key={idx} className="log-entry">
                  <span className="log-time">[{log.time}]</span>
                  <span className={`log-content log-type-${log.type}`}>
                    {typeof log.content === 'object' ? JSON.stringify(log.content) : log.content}
                  </span>
                </div>
              ))
            )}
            <div ref={consoleEndRef} />
          </div>
        </section>

        {/* Right Side: Parsed Multi-Tab Output Matrix Workspace */}
        <section className="glass-panel results-panel">
          <div className="tabs-header">
            <button
              type="button"
              className={`tab-btn ${activeTab === 'verdict' ? 'active' : ''}`}
              onClick={() => setActiveTab('verdict')}
            >
              FINAL VERDICT SCORECARD
            </button>
            <button
              type="button"
              className={`tab-btn ${activeTab === 'data' ? 'active' : ''}`}
              onClick={() => setActiveTab('data')}
            >
              COMPILED TEMPLATE DATA
            </button>
          </div>

          <div className="tab-content">
            {activeTab === 'verdict' ? (
              <div>
                {!jobState.verdict ? (
                  <div style={{ textAlign: 'center', padding: '4rem 1rem', color: 'var(--text-muted)' }}>
                    <ShieldAlert size={48} style={{ opacity: 0.3, marginBottom: '1rem' }} />
                    <p>Definitive scorecard matrix will render dynamically upon Phase 2 criteria calculation completion.</p>
                  </div>
                ) : (
                  <div>
                    <div className="verdict-header">
                      <div style={{ fontSize: '0.8rem', color: 'var(--text-muted)', fontWeight: 700, marginBottom: '4px' }}>
                        DEFINITIVE RECOMMENDATION
                      </div>
                      {renderVerdictBadge(jobState.verdict.verdict)}
                      <div className="price-target" style={{ marginTop: '0.5rem' }}>
                        Target Discount Entry Point: <strong>{jobState.verdict.target_entry_price || 'N/A'}</strong>
                      </div>
                      {jobState.verdict.reasoning && (
                        <p style={{ fontSize: '0.95rem', color: 'var(--text-secondary)', marginTop: '0.75rem', fontStyle: 'italic' }}>
                          "{jobState.verdict.reasoning}"
                        </p>
                      )}
                    </div>

                    {jobState.verdict.scores && (
                      <div className="scores-grid">
                        <div className="score-card">
                          <div className="score-label">Quality Integrity</div>
                          <div className="score-val" style={{ color: jobState.verdict.scores.quality?.includes('PASS') ? 'var(--success-color)' : 'var(--warning-color)' }}>
                            {jobState.verdict.scores.quality || 'N/A'}
                          </div>
                        </div>
                        <div className="score-card">
                          <div className="score-label">Valuation Trigger</div>
                          <div className="score-val">{jobState.verdict.scores.valuation || 'N/A'}</div>
                        </div>
                        <div className="score-card">
                          <div className="score-label">Business Moat</div>
                          <div className="score-val" style={{ color: 'var(--accent-color)' }}>{jobState.verdict.scores.moat || 'N/A'}</div>
                        </div>
                        <div className="score-card">
                          <div className="score-label">Management Outlook</div>
                          <div className="score-val">{jobState.verdict.scores.management || 'N/A'}</div>
                        </div>
                      </div>
                    )}

                    {jobState.verdict.checklist_log && Array.isArray(jobState.verdict.checklist_log) && (
                      <div>
                        <div style={{ fontSize: '0.8rem', color: 'var(--text-muted)', fontWeight: 700, marginTop: '1rem', marginBottom: '0.5rem', letterSpacing: '0.5px' }}>
                          CHECKLIST RULES COMPLIANCE MATRIX
                        </div>
                        <table className="checklist-table">
                          <thead>
                            <tr>
                              <th>Metric Trigger</th>
                              <th style={{ width: '120px', textAlign: 'center' }}>Status</th>
                              <th>Evaluation Context</th>
                            </tr>
                          </thead>
                          <tbody>
                            {jobState.verdict.checklist_log.map((item, i) => (
                              <tr key={i}>
                                <td style={{ fontWeight: 600, color: 'var(--text-primary)' }}>{item.metric}</td>
                                <td>{renderStatusIcon(item.status)}</td>
                                <td style={{ color: 'var(--text-secondary)' }}>{item.note}</td>
                              </tr>
                            ))}
                          </tbody>
                        </table>
                      </div>
                    )}

                    {jobState.verdict.raw && (
                      <div className="markdown-preview" style={{ background: 'rgba(0,0,0,0.3)', padding: '1rem', borderRadius: '8px', marginTop: '1rem' }}>
                        {jobState.verdict.raw}
                      </div>
                    )}
                  </div>
                )}
              </div>
            ) : (
              <div>
                {!jobState.gatheredData ? (
                  <div style={{ textAlign: 'center', padding: '4rem 1rem', color: 'var(--text-muted)' }}>
                    <HelpCircle size={48} style={{ opacity: 0.3, marginBottom: '1rem' }} />
                    <p>Phase 1 parameter data matrix output blocks are being compiled systematically via browsing tools...</p>
                  </div>
                ) : (
                  <div className="markdown-preview">
                    {jobState.gatheredData}
                  </div>
                )}
              </div>
            )}
          </div>
        </section>
      </main>
    </div>
  );
}
