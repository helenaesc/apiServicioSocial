INSERT INTO admin_users (full_name, email, password_hash, role, status)
VALUES (
  'Admin Principal',
  'admin@tuapp.com',
  'scrypt:32768:8:1$kRWGPibV9jmx7OHU$290429efa4c49f02ef7d4d309b5ecc03d95c131efa92ed49c1180ba7bd3df809227b9d82526806fc3f6f4a0923ac495302e846f1dfe13c417021cae87ae9a156',
  'ADMIN',
  'ACTIVE'
);

# pass = @dminKey1
