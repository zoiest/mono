//! Core domain models and value types for stock quotes and market data.

pub mod historical;
pub mod provider;
pub mod quote;

pub use historical::HistoricalPrice;
pub use provider::{ParseProviderError, ProviderType};
pub use quote::Quote;
