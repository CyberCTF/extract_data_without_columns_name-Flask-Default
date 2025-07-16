-- FinTrack Database Initialization
-- Column names are obfuscated to simulate real-world scenarios

USE fintrack_db;

-- Create users table with obfuscated column names
CREATE TABLE IF NOT EXISTS users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    xyz_username VARCHAR(50) NOT NULL UNIQUE,
    abc_password_hash VARCHAR(255) NOT NULL,
    def_email VARCHAR(100) NOT NULL,
    ghi_full_name VARCHAR(100) NOT NULL,
    jkl_role VARCHAR(50) DEFAULT 'user',
    mno_created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    pqr_last_login TIMESTAMP NULL,
    stu_department VARCHAR(50) DEFAULT 'General',
    vwx_is_active BOOLEAN DEFAULT TRUE
);

-- Create accounts table with obfuscated column names
CREATE TABLE IF NOT EXISTS accounts (
    id INT AUTO_INCREMENT PRIMARY KEY,
    aaa_account_name VARCHAR(100) NOT NULL,
    bbb_balance DECIMAL(15,2) DEFAULT 0.00,
    ccc_currency VARCHAR(3) DEFAULT 'USD',
    ddd_owner_id INT,
    eee_created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    fff_updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    ggg_status VARCHAR(20) DEFAULT 'active',
    hhh_account_type VARCHAR(50) DEFAULT 'checking',
    iii_description TEXT,
    jjj_is_primary BOOLEAN DEFAULT FALSE,
    FOREIGN KEY (ddd_owner_id) REFERENCES users(id)
);

-- Insert seed data
INSERT INTO users (xyz_username, abc_password_hash, def_email, ghi_full_name, jkl_role, stu_department) VALUES
('admin', '$2y$10$92IXUNpkjO0rOQ5byMi.Ye4oKoEa3Ro9llC/.og/at2.uheWG/igi', 'admin@fintrack.com', 'Administrator', 'admin', 'IT'),
('john.doe', '$2y$10$92IXUNpkjO0rOQ5byMi.Ye4oKoEa3Ro9llC/.og/at2.uheWG/igi', 'john.doe@fintrack.com', 'John Doe', 'user', 'Finance'),
('jane.smith', '$2y$10$92IXUNpkjO0rOQ5byMi.Ye4oKoEa3Ro9llC/.og/at2.uheWG/igi', 'jane.smith@fintrack.com', 'Jane Smith', 'manager', 'Marketing'),
('mike.wilson', '$2y$10$92IXUNpkjO0rOQ5byMi.Ye4oKoEa3Ro9llC/.og/at2.uheWG/igi', 'mike.wilson@fintrack.com', 'Mike Wilson', 'user', 'Sales'),
('sarah.jones', '$2y$10$92IXUNpkjO0rOQ5byMi.Ye4oKoEa3Ro9llC/.og/at2.uheWG/igi', 'sarah.jones@fintrack.com', 'Sarah Jones', 'user', 'HR'),
('david.brown', '$2y$10$92IXUNpkjO0rOQ5byMi.Ye4oKoEa3Ro9llC/.og/at2.uheWG/igi', 'david.brown@fintrack.com', 'David Brown', 'manager', 'Operations');

-- Insert account data
INSERT INTO accounts (aaa_account_name, bbb_balance, ccc_currency, ddd_owner_id, ggg_status, hhh_account_type, iii_description, jjj_is_primary) VALUES
('Main Operating Account', 125000.00, 'USD', 1, 'active', 'checking', 'Primary business account for daily operations', TRUE),
('Marketing Budget', 45000.00, 'USD', 3, 'active', 'savings', 'Dedicated account for marketing campaigns', FALSE),
('Sales Commission Pool', 78000.00, 'USD', 4, 'active', 'checking', 'Account for sales team commissions', FALSE),
('Emergency Fund', 200000.00, 'USD', 1, 'active', 'savings', 'Reserve fund for unexpected expenses', FALSE),
('Payroll Account', 95000.00, 'USD', 5, 'active', 'checking', 'Dedicated account for employee payroll', FALSE); 