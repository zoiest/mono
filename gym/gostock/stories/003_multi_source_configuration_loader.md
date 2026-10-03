# Story 003: Multi-Source Configuration Loader

## User Story
**As an** operator of `gostock`,  
**I want to** configure the application using command-line flags, environment variables, or a config file,  
**So that** configuration adheres to 12-factor principles with deterministic precedence: CLI Flags > Environment Variables > Config File > Defaults.

---

## 📖 Book Alignment
* **Book:** *Go in Practice, Second Edition*
* **Chapter:** Chapter 2: *A solid foundation: Building a command-line application*
* **Sections:**
  - 2.1 *Building CLI applications the Go way (Command-line flags)*
  - 2.2 *Handling configuration (Using configuration files, Configuration via environment variables)*

---

## 🎯 What You Will Learn
1. Using Go's standard `flag` package for parsing command-line parameters.
2. Reading environment variables with `os.LookupEnv` and parsing integers/durations.
3. Reading and unmarshaling JSON/YAML configuration files.
4. Implementing configuration hierarchy and default values idiomatically.

---

## 🛠️ Step-by-Step Implementation Guide

### 1. Define the Config Structure
In `internal/config/config.go`:
```go
package config

import (
	"encoding/json"
	"flag"
	"fmt"
	"os"
	"strconv"
	"time"
)

type Config struct {
	Port         int           `json:"port"`
	Timeout      time.Duration `json:"timeout"`
	Provider     string        `json:"provider"`
	CacheTTL     time.Duration `json:"cache_ttl"`
	MaxWorkers   int           `json:"max_workers"`
	RateLimitRPS int           `json:"rate_limit_rps"`
}

func DefaultConfig() Config {
	return Config{
		Port:         8080,
		Timeout:      5 * time.Second,
		Provider:     "yahoo",
		CacheTTL:     60 * time.Second,
		MaxWorkers:   5,
		RateLimitRPS: 10,
	}
}
```

### 2. Implement the Hierarchy Loader
In `internal/config/loader.go`:
```go
func Load(args []string) (*Config, error) {
	cfg := DefaultConfig()

	// 1. Load from optional config file if exists
	configFile := "config.json"
	if data, err := os.ReadFile(configFile); err == nil {
		if err := json.Unmarshal(data, &cfg); err != nil {
			return nil, fmt.Errorf("failed to parse %s: %w", configFile, err)
		}
	}

	// 2. Override with Environment Variables
	if val, ok := os.LookupEnv("GOSTOCK_PORT"); ok {
		if p, err := strconv.Atoi(val); err == nil {
			cfg.Port = p
		}
	}
	if val, ok := os.LookupEnv("GOSTOCK_PROVIDER"); ok {
		cfg.Provider = val
	}

	// 3. Override with CLI Flags
	fs := flag.NewFlagSet("gostock", flag.ContinueOnError)
	fs.IntVar(&cfg.Port, "port", cfg.Port, "HTTP server port")
	fs.StringVar(&cfg.Provider, "provider", cfg.Provider, "Default stock provider (yahoo, finviz, mock)")
	fs.DurationVar(&cfg.Timeout, "timeout", cfg.Timeout, "Request timeout duration")

	if err := fs.Parse(args); err != nil {
		return nil, err
	}

	return &cfg, nil
}
```

---

## ✅ Acceptance Criteria
- [ ] Running without arguments yields default configuration (`port=8080`, `provider=yahoo`).
- [ ] Setting `GOSTOCK_PORT=9000` overrides the default port.
- [ ] Passing `-port 9999` takes precedence over both environment variable and default.
- [ ] Unit tests in `internal/config/config_test.go` test precedence order.
