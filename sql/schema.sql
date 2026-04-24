CREATE TABLE IF NOT EXISTS leads (
    id BIGINT PRIMARY KEY AUTO_INCREMENT,
    company VARCHAR(255) NOT NULL,
    domain VARCHAR(255) NOT NULL UNIQUE,
    email VARCHAR(255) NULL,
    confidence FLOAT NULL,
    pitch TEXT NULL,
    short_pitch VARCHAR(500) NULL,
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_leads_domain (domain),
    INDEX idx_leads_created_at (created_at)
);

CREATE TABLE IF NOT EXISTS query_logs (
    id BIGINT PRIMARY KEY AUTO_INCREMENT,
    company VARCHAR(255) NOT NULL,
    domain VARCHAR(255) NOT NULL,
    email VARCHAR(255) NULL,
    confidence FLOAT NULL,
    pitch TEXT NULL,
    status VARCHAR(50) NOT NULL,
    error_message TEXT NULL,
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_query_logs_domain (domain),
    INDEX idx_query_logs_created_at (created_at)
);
