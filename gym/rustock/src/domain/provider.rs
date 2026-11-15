use std::fmt;
use std::str::FromStr;

use serde::{Deserialize, Serialize};

/// Supported upstream stock market data providers.
#[derive(Debug, Clone, Copy, PartialEq, Eq, Hash, Default, Serialize, Deserialize)]
#[serde(rename_all = "lowercase")]
pub enum ProviderType {
    #[default]
    Unknown,
    Yahoo,
    Finviz,
    Mock,
}

impl fmt::Display for ProviderType {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        let name = match self {
            ProviderType::Yahoo => "yahoo",
            ProviderType::Finviz => "finviz",
            ProviderType::Mock => "mock",
            ProviderType::Unknown => "unknown",
        };
        write!(f, "{name}")
    }
}

/// Error returned when parsing an unrecognized provider string.
#[derive(Debug, Clone, PartialEq, Eq)]
pub struct ParseProviderError {
    pub input: String,
}

impl fmt::Display for ParseProviderError {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        write!(f, "unknown provider: {}", self.input)
    }
}

impl std::error::Error for ParseProviderError {}

impl FromStr for ProviderType {
    type Err = ParseProviderError;

    fn from_str(s: &str) -> Result<Self, Self::Err> {
        match s.trim().to_ascii_lowercase().as_str() {
            "yahoo" => Ok(ProviderType::Yahoo),
            "finviz" => Ok(ProviderType::Finviz),
            "mock" => Ok(ProviderType::Mock),
            _ => Err(ParseProviderError {
                input: s.to_string(),
            }),
        }
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn display_formats_provider_names() {
        assert_eq!(ProviderType::Yahoo.to_string(), "yahoo");
        assert_eq!(ProviderType::Finviz.to_string(), "finviz");
        assert_eq!(ProviderType::Mock.to_string(), "mock");
        assert_eq!(ProviderType::Unknown.to_string(), "unknown");
    }

    #[test]
    fn from_str_parses_valid_providers() {
        assert_eq!("yahoo".parse::<ProviderType>(), Ok(ProviderType::Yahoo));
        assert_eq!("Finviz".parse::<ProviderType>(), Ok(ProviderType::Finviz));
        assert_eq!("MOCK".parse::<ProviderType>(), Ok(ProviderType::Mock));
    }

    #[test]
    fn from_str_rejects_unknown_provider() {
        let err = "bloomberg".parse::<ProviderType>().unwrap_err();
        assert_eq!(err.to_string(), "unknown provider: bloomberg");
    }
}
