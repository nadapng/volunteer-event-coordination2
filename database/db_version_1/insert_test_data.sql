SET FOREIGN_KEY_CHECKS=0;
SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

-- ADD YOUR CODE HERE ----
USE `volunteer_event_coordination`;

INSERT INTO users (full_name, email, phone, role) VALUES
('Nada Alamri','nada@example.com','+1-555-0101','organizer'),
('Sara Ali','sara@example.com',NULL,'volunteer'),
('Omar Z','omar@example.com',NULL,'volunteer')
ON DUPLICATE KEY UPDATE full_name=VALUES(full_name);

INSERT INTO events (title, description, location, starts_at, ends_at, capacity, created_by) VALUES
('Food Drive', 'Community food collection and sorting', 'Community Center',
 '2025-11-20 10:00:00','2025-11-20 14:00:00',50, 1),
('Park Cleanup', 'Clean-up of Riverside Park', 'Riverside Park',
 '2025-11-22 09:00:00','2025-11-22 12:30:00',30, 1);

INSERT INTO volunteer_shift_xref (event_id, user_id, status) VALUES
(1, 2, 'registered'),
(1, 3, 'registered'),
(2, 2, 'waitlist')
ON DUPLICATE KEY UPDATE status=VALUES(status);


COMMIT;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;