/*
 Navicat Premium Dump SQL

 Source Server         : StudentDatabase
 Source Server Type    : MySQL
 Source Server Version : 90200 (9.2.0)
 Source Host           : localhost:3306
 Source Schema         : studentmanagement

 Target Server Type    : MySQL
 Target Server Version : 90200 (9.2.0)
 File Encoding         : 65001

 Date: 03/05/2025 14:51:45
*/

SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
-- Table structure for coursechoosing
-- ----------------------------
DROP TABLE IF EXISTS `coursechoosing`;
CREATE TABLE `coursechoosing`  (
  `StudentID` char(10) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `CourseID` char(7) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `TeacherID` char(5) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `ChosenYear` int NOT NULL,
  `Score` decimal(3, 1) NULL DEFAULT NULL,
  PRIMARY KEY (`StudentID`, `CourseID`, `TeacherID`) USING BTREE,
  INDEX `fk_course`(`CourseID` ASC) USING BTREE,
  INDEX `fk_teacher`(`TeacherID` ASC) USING BTREE,
  CONSTRAINT `fk_course` FOREIGN KEY (`CourseID`) REFERENCES `courses` (`CourseID`) ON DELETE CASCADE ON UPDATE RESTRICT,
  CONSTRAINT `fk_student` FOREIGN KEY (`StudentID`) REFERENCES `students` (`StudentID`) ON DELETE CASCADE ON UPDATE RESTRICT,
  CONSTRAINT `fk_teacher` FOREIGN KEY (`TeacherID`) REFERENCES `teachers` (`TeacherID`) ON DELETE CASCADE ON UPDATE RESTRICT
) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = Dynamic;

SET FOREIGN_KEY_CHECKS = 1;
