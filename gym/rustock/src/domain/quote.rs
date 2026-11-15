use chrono::{DateTime, Utc};
use serde::{Deserialize, Serialize};

use super::provider::ProviderType;

/// Real-time or delayed stock quote for a single ticker symbol.
#[derive(Debug, Clone, PartialEq, Serialize, Deserialize)]
pub struct Quote {
    pub symbol: String,
    #[serde(default, skip_serializing_if = "Option::is_none")]
    pub company_name: Option<String>,
    pub price: f64,
    #[serde(default, skip_serializing_if = "Option::is_none")]
    pub previous_close: Option<f64>,
    #[serde(default, skip_serializing_if = "Option::is_none")]
    pub open: Option<f64>,
    #[serde(default, skip_serializing_if = "Option::is_none")]
    pub day_high: Option<f64>,
    #[serde(default, skip_serializing_if = "Option::is_none")]
    pub day_low: Option<f64>,
    #[serde(default, skip_serializing_if = "Option::is_none")]
    pub volume: Option<u64>,
    pub provider: ProviderType,
    #[serde(default = "Utc::now")]
    pub updated_at: DateTime<Utc>,
}

impl Quote {
    /// Returns the absolute price change relative to `previous_close`.
    pub fn change(&self) -> f64 {
        match self.previous_close {
            Some(prev) if prev != 0.0 => self.price - prev,
            _ => 0.0,
        }
    }

    /// Returns the percentage price change relative to `previous_close`.
    pub fn change_percent(&self) -> f64 {
        match self.previous_close {
            Some(prev) if prev != 0.0 => (self.change() / prev) * 100.0,
            _ => 0.0,
        }
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    fn sample_quote(price: f64, previous_close: Option<f64>) -> Quote {
        Quote {
            symbol: "AAPL".to_string(),
            company_name: None,
            price,
            previous_close,
            open: None,
            day_high: None,
            day_low: None,
            volume: None,
            provider: ProviderType::Yahoo,
            updated_at: Utc::now(),
        }
    }

    #[test]
    fn change_and_percent_calculations() {
        let cases = [
            ("gain in price", 110.0, Some(100.0), 10.0, 10.0),
            ("loss in price", 90.0, Some(100.0), -10.0, -10.0),
            ("zero previous close", 100.0, Some(0.0), 0.0, 0.0),
            ("missing previous close", 100.0, None, 0.0, 0.0),
        ];

        for (name, price, prev, want_change, want_pct) in cases {
            let quote = sample_quote(price, prev);
            assert!(
                (quote.change() - want_change).abs() < 1e-9,
                "{name}: got change {}, want {want_change}",
                quote.change()
            );
            assert!(
                (quote.change_percent() - want_pct).abs() < 1e-9,
                "{name}: got change_percent {}, want {want_pct}",
                quote.change_percent()
            );
        }
    }

    #[test]
    fn json_serialization_omits_none_fields() {
        let quote = sample_quote(150.0, None);
        let json = serde_json::to_string(&quote).expect("serialize quote");

        assert!(json.contains(r#""symbol":"AAPL""#));
        assert!(json.contains(r#""provider":"yahoo""#));
        assert!(!json.contains("company_name"));
        assert!(!json.contains("volume"));
    }

    #[test]
    fn json_deserialization_populates_fields() {
        let raw_json = r#"{
            "symbol": "MSFT",
            "company_name": "Microsoft Corp",
            "price": 310.5,
            "previous_close": 305.0,
            "provider": "yahoo"
        }"#;

        let quote: Quote = serde_json::from_str(raw_json).expect("deserialize quote");
        assert_eq!(quote.symbol, "MSFT");
        assert_eq!(quote.company_name.as_deref(), Some("Microsoft Corp"));
        assert_eq!(quote.price, 310.5);
        assert_eq!(quote.previous_close, Some(305.0));
        assert_eq!(quote.provider, ProviderType::Yahoo);
    }
}
