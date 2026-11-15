use chrono::{DateTime, Utc};
use serde::{Deserialize, Serialize};

/// Historical OHLCV (Open, High, Low, Close, Volume) price bar.
#[derive(Debug, Clone, PartialEq, Serialize, Deserialize)]
pub struct HistoricalPrice {
    pub date: DateTime<Utc>,
    pub open: f64,
    pub high: f64,
    pub low: f64,
    pub close: f64,
    pub volume: u64,
}
