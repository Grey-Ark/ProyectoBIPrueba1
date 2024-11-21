-- MySQL Workbench Forward Engineering

SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION';

-- -----------------------------------------------------
-- Schema nutriologo
-- -----------------------------------------------------

-- -----------------------------------------------------
-- Schema nutriologo
-- -----------------------------------------------------
CREATE SCHEMA IF NOT EXISTS `nutriologo` DEFAULT CHARACTER SET utf8 ;
USE `nutriologo` ;

-- -----------------------------------------------------
-- Table `nutriologo`.`Genero`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `nutriologo`.`Genero` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `Genero` VARCHAR(45) NULL,
  PRIMARY KEY (`id`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `nutriologo`.`Objetivo`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `nutriologo`.`Objetivo` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `Objetivo` VARCHAR(150) NULL,
  PRIMARY KEY (`id`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `nutriologo`.`IdRegimen`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `nutriologo`.`IdRegimen` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `IdRegimen` VARCHAR(45) NULL,
  PRIMARY KEY (`id`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `nutriologo`.`NombreRegimen`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `nutriologo`.`NombreRegimen` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `NombreRegimen` VARCHAR(150) NULL,
  PRIMARY KEY (`id`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `nutriologo`.`CostoRegimen`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `nutriologo`.`CostoRegimen` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `CostoRegimen` INT NULL,
  PRIMARY KEY (`id`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `nutriologo`.`RangoCosto`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `nutriologo`.`RangoCosto` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `RangoCosto` VARCHAR(45) NULL,
  PRIMARY KEY (`id`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `nutriologo`.`PorcionesDesayuno`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `nutriologo`.`PorcionesDesayuno` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `PorcionesDesayuno` INT NULL,
  PRIMARY KEY (`id`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `nutriologo`.`PorcionesAlmuerzo`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `nutriologo`.`PorcionesAlmuerzo` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `PorcionesAlmuerzo` INT NULL,
  PRIMARY KEY (`id`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `nutriologo`.`PorcionesCena`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `nutriologo`.`PorcionesCena` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `PorcionesCena` INT NULL,
  PRIMARY KEY (`id`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `nutriologo`.`PorcionesColacion1`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `nutriologo`.`PorcionesColacion1` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `PorcionesColacion1` INT NULL,
  PRIMARY KEY (`id`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `nutriologo`.`PorcionesColacion2`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `nutriologo`.`PorcionesColacion2` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `PorcionesColacion2` INT NULL,
  `PorcionesColacion2col` VARCHAR(45) NULL,
  PRIMARY KEY (`id`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `nutriologo`.`IngestaRealDesayuno`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `nutriologo`.`IngestaRealDesayuno` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `IngestaRealDesayuno` INT NULL,
  PRIMARY KEY (`id`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `nutriologo`.`IngestaRealAlmuerzo`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `nutriologo`.`IngestaRealAlmuerzo` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `IngestaRealAlmuerzo` INT NULL,
  PRIMARY KEY (`id`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `nutriologo`.`IngestaRealCena`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `nutriologo`.`IngestaRealCena` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `IngestaRealCena` INT NULL,
  PRIMARY KEY (`id`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `nutriologo`.`IngestaRealColacion1`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `nutriologo`.`IngestaRealColacion1` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `IngestaRealColacion1` INT NULL,
  PRIMARY KEY (`id`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `nutriologo`.`IngestaRealColacion2`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `nutriologo`.`IngestaRealColacion2` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `IngestaRealColacion2` INT NULL,
  PRIMARY KEY (`id`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `nutriologo`.`SatisfaccionPaciente`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `nutriologo`.`SatisfaccionPaciente` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `SatisfaccionPaciente` INT NULL,
  PRIMARY KEY (`id`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `nutriologo`.`EstadoPaciente`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `nutriologo`.`EstadoPaciente` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `EstadoPaciente` VARCHAR(45) NULL,
  PRIMARY KEY (`id`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `nutriologo`.`CitasAgendadas`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `nutriologo`.`CitasAgendadas` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `CitasAgendadas` INT NULL,
  PRIMARY KEY (`id`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `nutriologo`.`CitasAsistidas`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `nutriologo`.`CitasAsistidas` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `CitasAsistidas` INT NULL,
  PRIMARY KEY (`id`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `nutriologo`.`Paciente`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `nutriologo`.`Paciente` (
  `idPaciente` INT NOT NULL AUTO_INCREMENT,
  `Nombre` VARCHAR(150) NULL,
  `Edad` INT NULL,
  `idGenero` INT NOT NULL,
  `PesoInicial` DECIMAL(4) NULL,
  `Altura` DECIMAL(4) NULL,
  `IMC` DECIMAL(7) NULL,
  `idObjetivo` INT NOT NULL,
  `idRegimen` INT NOT NULL,
  `idNombreRegimen` INT NOT NULL,
  `idCostoRegimen` INT NOT NULL,
  `idRangoCosto` INT NOT NULL,
  `FechaInicioRegimen` DATE NOT NULL,
  `FechaFinRegimen` DATE NOT NULL,
  `idPorcionesDesayuno` INT NOT NULL,
  `idPorcionesAlmuerzo` INT NOT NULL,
  `idPorcionesCena` INT NOT NULL,
  `idPorcionesColacion1` INT NOT NULL,
  `idPorcionesColacion2` INT NOT NULL,
  `idIngestaRealDesayuno` INT NOT NULL,
  `idIngestaRealAlmuerzo` INT NOT NULL,
  `idIngestaRealCena` INT NOT NULL,
  `idIngestaRealColacion1` INT NOT NULL,
  `idIngestaRealColacion2` INT NOT NULL,
  `PesoActual` DECIMAL(4) NULL,
  `idSatisfaccionPaciente` INT NOT NULL,
  `idEstadoPaciente` INT NOT NULL,
  `idCitasAgendadas` INT NOT NULL,
  `idCitasAsistidas` INT NOT NULL,
  PRIMARY KEY (`idPaciente`),
  INDEX `fk_Paciente_Genero_idx` (`idGenero` ASC) VISIBLE,
  INDEX `fk_Paciente_Objetivo1_idx` (`idObjetivo` ASC) VISIBLE,
  INDEX `fk_Paciente_IdRegimen1_idx` (`idRegimen` ASC) VISIBLE,
  INDEX `fk_Paciente_NombreRegimen1_idx` (`idNombreRegimen` ASC) VISIBLE,
  INDEX `fk_Paciente_CostoRegimen1_idx` (`idCostoRegimen` ASC) VISIBLE,
  INDEX `fk_Paciente_RangoCosto1_idx` (`idRangoCosto` ASC) VISIBLE,
  INDEX `fk_Paciente_PorcionesDesayuno1_idx` (`idPorcionesDesayuno` ASC) VISIBLE,
  INDEX `fk_Paciente_PorcionesAlmuerzo1_idx` (`idPorcionesAlmuerzo` ASC) VISIBLE,
  INDEX `fk_Paciente_PorcionesCena1_idx` (`idPorcionesCena` ASC) VISIBLE,
  INDEX `fk_Paciente_PorcionesColacion11_idx` (`idPorcionesColacion1` ASC) VISIBLE,
  INDEX `fk_Paciente_PorcionesColacion21_idx` (`idPorcionesColacion2` ASC) VISIBLE,
  INDEX `fk_Paciente_IngestaRealDesayuno1_idx` (`idIngestaRealDesayuno` ASC) VISIBLE,
  INDEX `fk_Paciente_IngestaRealAlmuerzo1_idx` (`idIngestaRealAlmuerzo` ASC) VISIBLE,
  INDEX `fk_Paciente_IngestaRealCena1_idx` (`idIngestaRealCena` ASC) VISIBLE,
  INDEX `fk_Paciente_IngestaRealColacion11_idx` (`idIngestaRealColacion1` ASC) VISIBLE,
  INDEX `fk_Paciente_IngestaRealColacion21_idx` (`idIngestaRealColacion2` ASC) VISIBLE,
  INDEX `fk_Paciente_SatisfaccionPaciente1_idx` (`idSatisfaccionPaciente` ASC) VISIBLE,
  INDEX `fk_Paciente_EstadoPaciente1_idx` (`idEstadoPaciente` ASC) VISIBLE,
  INDEX `fk_Paciente_CitasAgendadas1_idx` (`idCitasAgendadas` ASC) VISIBLE,
  INDEX `fk_Paciente_CitasAsistidas1_idx` (`idCitasAsistidas` ASC) VISIBLE)
ENGINE = InnoDB;


SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;
