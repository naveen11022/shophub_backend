-- Fix enum values in users table
ALTER TABLE users MODIFY COLUMN role ENUM('admin', 'user') DEFAULT 'user';

-- Fix enum values in orders table  
ALTER TABLE orders MODIFY COLUMN status ENUM('pending', 'confirmed', 'processing', 'shipped', 'delivered', 'cancelled') DEFAULT 'pending';
