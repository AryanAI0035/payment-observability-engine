import { useState, useEffect } from 'react';
import axios from 'axios';
import { Activity, AlertCircle, CheckCircle, BrainCircuit } from 'lucide-react';
import './index.css';

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

function App() {
  const [transactions, setTransactions] = useState([]);
  const [selectedTx, setSelectedTx] = useState(null);
  const [analysis, setAnalysis] = useState(null);
  const [loadingAnalysis, setLoadingAnalysis] = useState(false);

  useEffect(() => {
    const fetchTransactions = async () => {
      try {
        const res = await axios.get(`${API_URL}/api/transactions`);
        setTransactions(res.data);
      } catch (error) {
        console.error("Error fetching transactions", error);
      }
    };
    fetchTransactions();
    const interval = setInterval(fetchTransactions, 2000);
    return () => clearInterval(interval);
  }, []);

  const handleSelectTx = async (tx) => {
    setSelectedTx(tx);
    if (tx.status === 'FAILED') {
      setLoadingAnalysis(true);
      setAnalysis(null);
      try {
        let fetched = false;
        for (let i = 0; i < 10; i++) {
          try {
            const res = await axios.get(`${API_URL}/api/analysis/${tx.id}`);
            if (res.data) {
              setAnalysis(res.data);
              fetched = true;
              break;
            }
          } catch (e) {
            await new Promise(r => setTimeout(r, 1000));
          }
        }
      } catch (error) {
        console.error("Analysis failed", error);
      } finally {
        setLoadingAnalysis(false);
      }
    } else {
      setAnalysis(null);
    }
  };

  return (
    <div className="app-container">
      <header className="header">
        <Activity color="#3b82f6" size={32} />
        <h1>Omni<span>Pay</span> Agentic Observability</h1>
      </header>

      <div className="dashboard-grid">
        <div className="card">
          <h2 className="card-title">
            <div className="status-indicator" style={{ marginRight: '12px' }}>
              <span className="ping"></span>
              <span className="dot"></span>
            </div>
            Live Transaction Stream
          </h2>
          
          <div style={{ overflowX: 'auto' }}>
            <table className="tx-table">
              <thead>
                <tr>
                  <th>TX ID</th>
                  <th>Merchant</th>
                  <th>Amount</th>
                  <th>Status</th>
                </tr>
              </thead>
              <tbody>
                {transactions.map((tx) => (
                  <tr 
                    key={tx.id} 
                    onClick={() => handleSelectTx(tx)}
                    className={`tx-row ${selectedTx?.id === tx.id ? 'selected' : ''}`}
                  >
                    <td className="font-mono">{tx.id}</td>
                    <td style={{ fontWeight: 500 }}>{tx.merchant}</td>
                    <td className="font-mono">${tx.amount.toFixed(2)}</td>
                    <td>
                      {tx.status === 'SUCCESS' ? (
                        <span className="status-badge status-success">
                          <CheckCircle size={14} /> Success
                        </span>
                      ) : (
                        <span className="status-badge status-failed">
                          <AlertCircle size={14} /> Failed
                        </span>
                      )}
                    </td>
                  </tr>
                ))}
                {transactions.length === 0 && (
                  <tr>
                    <td colSpan="4" style={{ padding: '2rem 0', textAlign: 'center', color: 'var(--text-muted)' }}>
                      Waiting for transactions...
                    </td>
                  </tr>
                )}
              </tbody>
            </table>
          </div>
        </div>

        <div className="card" style={{ height: 'fit-content' }}>
          <h2 className="card-title">
            <BrainCircuit color="#a855f7" size={24} style={{ marginRight: '12px' }} />
            Agentic Root Cause Analysis
          </h2>
          
          {!selectedTx ? (
            <div className="empty-state">
              Select a failed transaction to view AI analysis.
            </div>
          ) : selectedTx.status === 'SUCCESS' ? (
            <div className="success-state">
              Transaction successful. No anomalies detected.
            </div>
          ) : (
            <div>
              <div className="tx-header-box">
                <div className="tx-id">TX: {selectedTx.id}</div>
                <div className="tx-amount">{selectedTx.merchant} - ${selectedTx.amount.toFixed(2)}</div>
              </div>

              {loadingAnalysis ? (
                <div className="loader-container">
                  <div className="spinner"></div>
                  <div className="pulse-text">Agentic AI diagnosing failure logs...</div>
                </div>
              ) : analysis ? (
                <div className="analysis-box">
                  <div className="insight-card reason">
                    <div className="insight-title">Identified Root Cause</div>
                    <div className="insight-content">{analysis.reason}</div>
                  </div>
                  <div className="insight-card action">
                    <div className="insight-title">Recommended Action</div>
                    <div className="insight-content">{analysis.recommended_action}</div>
                  </div>
                  <div className="analysis-footer">
                    <span>Model: Gemini 2.5 Pro (RAG)</span>
                    <span className="confidence">
                      <span className="confidence-dot"></span>
                      Confidence: {(analysis.confidence * 100).toFixed(0)}%
                    </span>
                  </div>
                </div>
              ) : (
                <div className="empty-state" style={{ border: 'none' }}>
                  Analysis unavailable.
                </div>
              )}
            </div>
          )}
        </div>
      </div>
    </div>
  );
}

export default App;
