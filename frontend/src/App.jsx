import React, { useEffect, useState } from "react";
import { ArrowUp, ArrowDown, RefreshCw, Info, BookOpen } from "lucide-react";

const API_BASE = import.meta.env.VITE_API_BASE || "http://localhost:8000";

const COLORS = {
  bg: "#12151A",
  panel: "#1A1E26",
  panelBorder: "#2B303B",
  amber: "#F0B429",
  green: "#2FBF71",
  red: "#E5484D",
  slate: "#8A94A6",
  offwhite: "#EDEFF3",
};

const FONT_DISPLAY = "'Space Grotesk', sans-serif";
const FONT_MONO = "'IBM Plex Mono', monospace";

function ScoreBar({ score }) {
  const pct = Math.min(Math.abs(score), 100);
  const color = score >= 0 ? COLORS.green : COLORS.red;
  return (
    <div style={{ display: "flex", alignItems: "center", gap: 8 }}>
      <div style={{ width: 70, height: 6, background: "#2B303B", borderRadius: 3, overflow: "hidden" }}>
        <div style={{ width: `${pct}%`, height: "100%", background: color }} />
      </div>
      <span style={{ fontFamily: FONT_MONO, fontSize: 12, color, fontWeight: 600 }}>
        {score > 0 ? "+" : ""}
        {score}
      </span>
    </div>
  );
}

function MacroStrip({ macro }) {
  if (!macro) return null;
  const items = Object.entries(macro).filter(([, v]) => v.ok);
  return (
    <div style={{ display: "flex", gap: 12, flexWrap: "wrap", marginBottom: 20 }}>
      {items.map(([key, m]) => (
        <div key={key} style={{ background: COLORS.panel, border: `1px solid ${COLORS.panelBorder}`, borderRadius: 8, padding: "8px 14px", minWidth: 120 }}>
          <div style={{ fontSize: 10, color: COLORS.slate, fontFamily: FONT_MONO, textTransform: "uppercase" }}>{m.label}</div>
          <div style={{ fontFamily: FONT_MONO, fontSize: 14, fontWeight: 600 }}>{m.value?.toLocaleString("en-IN")}</div>
          <div style={{ fontFamily: FONT_MONO, fontSize: 11, color: m.day_change_pct >= 0 ? COLORS.green : COLORS.red }}>
            {m.day_change_pct >= 0 ? "+" : ""}
            {m.day_change_pct}% today
          </div>
        </div>
      ))}
    </div>
  );
}

function MacroLinkRow({ link }) {
  const dirColor = link.expected_direction === "positive" ? COLORS.green : COLORS.red;
  return (
    <div style={{ padding: "6px 0", borderBottom: `1px solid ${COLORS.panelBorder}` }}>
      <div style={{ display: "flex", justifyContent: "space-between", fontSize: 12 }}>
        <span>
          <strong>{link.macro}</strong>{" "}
          <span style={{ color: dirColor }}>({link.expected_direction} link)</span>
        </span>
        <span style={{ color: COLORS.slate, fontFamily: FONT_MONO }}>
          corr: {link.computed_correlation_60d}{" "}
          {link.matches_typical_pattern ? "✓ holding" : "· not holding right now"}
        </span>
      </div>
      <div style={{ fontSize: 11.5, color: COLORS.slate, marginTop: 2 }}>{link.note}</div>
    </div>
  );
}

function StockRow({ stock }) {
  const [expanded, setExpanded] = useState(false);
  const up = stock.day_change_pct >= 0;

  return (
    <div style={{ background: COLORS.panel, border: `1px solid ${COLORS.panelBorder}`, borderRadius: 8, padding: "12px 16px", marginBottom: 10 }}>
      <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", flexWrap: "wrap", gap: 8 }}>
        <div style={{ minWidth: 170 }}>
          <div style={{ fontWeight: 600, fontSize: 15 }}>
            {stock.ticker} <span style={{ fontSize: 10, color: COLORS.amber, fontFamily: FONT_MONO }}>{stock.market}</span>
          </div>
          <div style={{ fontSize: 11.5, color: COLORS.slate }}>
            {stock.name} · {stock.sector}
          </div>
        </div>

        <div style={{ fontFamily: FONT_MONO, fontSize: 15, minWidth: 90 }}>
          {stock.market === "IN" ? "₹" : "$"}
          {stock.price?.toLocaleString("en-IN")}
        </div>

        <div style={{ minWidth: 90, display: "flex", alignItems: "center", gap: 4, color: up ? COLORS.green : COLORS.red, fontFamily: FONT_MONO, fontSize: 13 }}>
          {up ? <ArrowUp size={12} /> : <ArrowDown size={12} />}
          {Math.abs(stock.day_change_pct)}%
        </div>

        <ScoreBar score={stock.composite_score} />

        <div style={{ fontFamily: FONT_MONO, fontSize: 12, color: COLORS.slate, minWidth: 160 }}>
          Range {stock.market === "IN" ? "₹" : "$"}
          {stock.projected_range?.low} - {stock.projected_range?.high}
        </div>

        <button
          onClick={() => setExpanded(!expanded)}
          style={{ background: "none", border: `1px solid ${COLORS.panelBorder}`, color: COLORS.amber, borderRadius: 6, padding: "4px 10px", fontSize: 11, cursor: "pointer" }}
        >
          {expanded ? "Hide" : "Why?"}
        </button>
      </div>

      {expanded && (
        <div style={{ marginTop: 10, paddingTop: 10, borderTop: `1px solid ${COLORS.panelBorder}`, fontSize: 12.5 }}>
          <div style={{ display: "flex", gap: 20, marginBottom: 10, color: COLORS.slate, flexWrap: "wrap" }}>
            <span>Technical: {stock.technical_score}</span>
            <span>News: {stock.news_score} ({stock.headline_count} headlines)</span>
            <span>Macro: {stock.macro_score}</span>
            <span>RSI: {stock.rsi}</span>
            <span>MACD hist: {stock.macd_histogram}</span>
          </div>

          {stock.macro_links?.length > 0 && (
            <div style={{ marginBottom: 10 }}>
              <div style={{ fontSize: 11, color: COLORS.amber, textTransform: "uppercase", marginBottom: 4 }}>Macro drivers for this sector</div>
              {stock.macro_links.map((l, i) => (
                <MacroLinkRow key={i} link={l} />
              ))}
            </div>
          )}

          {stock.headlines?.length > 0 && (
            <div style={{ marginBottom: 10 }}>
              <div style={{ fontSize: 11, color: COLORS.amber, textTransform: "uppercase", marginBottom: 4 }}>Recent headlines</div>
              <ul style={{ margin: 0, paddingLeft: 18, color: COLORS.offwhite, opacity: 0.85, lineHeight: 1.6 }}>
                {stock.headlines.map((h, i) => (
                  <li key={i}>
                    {h.title} <span style={{ color: COLORS.slate }}>— {h.source}</span>
                  </li>
                ))}
              </ul>
            </div>
          )}

          {stock.related_historical_patterns?.length > 0 && (
            <div>
              <div style={{ fontSize: 11, color: COLORS.amber, textTransform: "uppercase", marginBottom: 4, display: "flex", alignItems: "center", gap: 4 }}>
                <BookOpen size={12} /> Related history
              </div>
              {stock.related_historical_patterns.map((p) => (
                <div key={p.id} style={{ fontSize: 12, color: COLORS.slate, marginBottom: 4 }}>
                  <strong style={{ color: COLORS.offwhite }}>{p.title}:</strong> {p.lesson}
                </div>
              ))}
            </div>
          )}
        </div>
      )}
    </div>
  );
}

function HistoricalPatternsPanel({ patterns }) {
  const [openId, setOpenId] = useState(null);
  return (
    <div style={{ marginTop: 32 }}>
      <h2 style={{ fontSize: 16, marginBottom: 10, display: "flex", alignItems: "center", gap: 6 }}>
        <BookOpen size={16} color={COLORS.amber} /> How news has actually moved markets before
      </h2>
      {patterns.map((p) => (
        <div key={p.id} style={{ background: COLORS.panel, border: `1px solid ${COLORS.panelBorder}`, borderRadius: 8, padding: "12px 16px", marginBottom: 8 }}>
          <div
            onClick={() => setOpenId(openId === p.id ? null : p.id)}
            style={{ cursor: "pointer", display: "flex", justifyContent: "space-between" }}
          >
            <strong>{p.title}</strong>
            <span style={{ color: COLORS.slate, fontFamily: FONT_MONO, fontSize: 11 }}>{p.period}</span>
          </div>
          {openId === p.id && (
            <div style={{ marginTop: 10, fontSize: 13, lineHeight: 1.6, color: COLORS.offwhite, opacity: 0.9 }}>
              <p><strong>Trigger:</strong> {p.trigger}</p>
              <p><strong>What happened:</strong> {p.market_impact}</p>
              <p><strong>Why:</strong> {p.mechanism}</p>
              <p style={{ color: COLORS.amber }}><strong>Takeaway:</strong> {p.lesson}</p>
            </div>
          )}
        </div>
      ))}
    </div>
  );
}

export default function App() {
  const [data, setData] = useState(null);
  const [patterns, setPatterns] = useState([]);
  const [marketFilter, setMarketFilter] = useState("ALL");
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  const load = async () => {
    setLoading(true);
    setError(null);
    try {
      const [moversRes, patternsRes] = await Promise.all([
        fetch(`${API_BASE}/api/movers`),
        fetch(`${API_BASE}/api/historical-patterns`),
      ]);
      if (!moversRes.ok) throw new Error(`API returned ${moversRes.status}`);
      setData(await moversRes.json());
      if (patternsRes.ok) setPatterns((await patternsRes.json()).patterns);
    } catch (e) {
      setError(e.message);
    } finally {
      setLoading(false);
    }
  };

  const manualRefresh = async () => {
    setLoading(true);
    try {
      await fetch(`${API_BASE}/api/refresh`);
      await load();
    } catch (e) {
      setError(e.message);
      setLoading(false);
    }
  };

  useEffect(() => {
    load();
  }, []);

  const filterByMarket = (list) => {
    if (!list) return [];
    if (marketFilter === "ALL") return list;
    if (marketFilter === "IN") return list.filter((s) => s.market === "IN");
    return list.filter((s) => s.market !== "IN");
  };

  return (
    <div style={{ background: COLORS.bg, minHeight: "100vh", color: COLORS.offwhite, fontFamily: FONT_DISPLAY, padding: 28 }}>
      <link href="https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@500;600;700&family=IBM+Plex+Mono:wght@400;500;600&display=swap" rel="stylesheet" />

      <div style={{ display: "flex", justifyContent: "space-between", alignItems: "flex-end", flexWrap: "wrap", gap: 12, marginBottom: 16 }}>
        <div>
          <div style={{ fontSize: 12, letterSpacing: 1.5, color: COLORS.amber, textTransform: "uppercase" }}>Global momentum tracker</div>
          <h1 style={{ fontSize: 26, fontWeight: 700, margin: "4px 0 0" }}>Today's expected movers</h1>
        </div>
        <div style={{ display: "flex", alignItems: "center", gap: 12 }}>
          <span style={{ fontFamily: FONT_MONO, fontSize: 11, color: COLORS.slate }}>
            {data?.generated_at ? `Updated ${new Date(data.generated_at).toLocaleString("en-IN")}` : "—"}
          </span>
          <button onClick={manualRefresh} style={{ display: "flex", alignItems: "center", gap: 6, background: "none", border: `1px solid ${COLORS.panelBorder}`, color: COLORS.offwhite, borderRadius: 6, padding: "6px 12px", cursor: "pointer" }}>
            <RefreshCw size={13} /> Refresh
          </button>
        </div>
      </div>

      <div style={{ display: "flex", gap: 10, background: "#241C10", border: "1px solid #4A3418", borderRadius: 8, padding: "12px 16px", marginBottom: 20, fontSize: 12.5, color: "#F0C77A", lineHeight: 1.55 }}>
        <Info size={16} style={{ flexShrink: 0, marginTop: 2 }} />
        <span>
          Rankings combine technical momentum, news sentiment, and each sector's actual computed correlation to
          relevant macro drivers (oil, currency, rates, global indices). The "range" is a statistical band from
          recent volatility, not a guaranteed price. Note: rising oil doesn't uniformly help Indian stocks - it
          hurts net importers and the broad market while helping specific upstream producers. This is a research
          aid, not financial advice, and has not been backtested for real predictive accuracy.
        </span>
      </div>

      <MacroStrip macro={data?.macro_snapshot} />

      <div style={{ display: "flex", gap: 8, marginBottom: 16 }}>
        {["ALL", "IN", "GLOBAL"].map((f) => (
          <button
            key={f}
            onClick={() => setMarketFilter(f)}
            style={{
              background: marketFilter === f ? COLORS.amber : "none",
              color: marketFilter === f ? "#12151A" : COLORS.offwhite,
              border: `1px solid ${COLORS.panelBorder}`,
              borderRadius: 6,
              padding: "6px 14px",
              fontSize: 12,
              cursor: "pointer",
              fontWeight: 600,
            }}
          >
            {f === "ALL" ? "All markets" : f === "IN" ? "India" : "Global"}
          </button>
        ))}
      </div>

      {loading && <div style={{ color: COLORS.slate }}>Loading...</div>}
      {error && (
        <div style={{ color: COLORS.red }}>
          Error: {error}. Is the backend running at {API_BASE}?
        </div>
      )}

      {data && !loading && (
        <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: 24 }}>
          <div>
            <h2 style={{ fontSize: 16, color: COLORS.green, marginBottom: 10 }}>Top expected gainers</h2>
            {filterByMarket(data.top_gainers).map((s) => (
              <StockRow key={s.ticker} stock={s} />
            ))}
          </div>
          <div>
            <h2 style={{ fontSize: 16, color: COLORS.red, marginBottom: 10 }}>Top expected losers</h2>
            {filterByMarket(data.top_losers).map((s) => (
              <StockRow key={s.ticker} stock={s} />
            ))}
          </div>
        </div>
      )}

      {patterns.length > 0 && <HistoricalPatternsPanel patterns={patterns} />}
    </div>
  );
}
