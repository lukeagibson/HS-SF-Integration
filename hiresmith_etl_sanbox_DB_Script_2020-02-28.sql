-- MySQL Workbench Forward Engineering

SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='TRADITIONAL,ALLOW_INVALID_DATES';

-- -----------------------------------------------------
-- Schema mydb
-- -----------------------------------------------------
-- -----------------------------------------------------
-- Schema hiresmith_etl_sandbox
-- -----------------------------------------------------

-- -----------------------------------------------------
-- Schema hiresmith_etl_sandbox
-- -----------------------------------------------------
CREATE SCHEMA IF NOT EXISTS `hiresmith_etl_sandbox` DEFAULT CHARACTER SET latin1 ;
USE `hiresmith_etl_sandbox` ;

-- -----------------------------------------------------
-- Table `hiresmith_etl_sandbox`.`hiresmith_account_manager`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `hiresmith_etl_sandbox`.`hiresmith_account_manager` (
  `account_manager_id` DOUBLE NOT NULL,
  `account_manager_value` VARCHAR(255) NOT NULL,
  PRIMARY KEY (`account_manager_id`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = latin1;


-- -----------------------------------------------------
-- Table `hiresmith_etl_sandbox`.`hiresmith_approval_status`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `hiresmith_etl_sandbox`.`hiresmith_approval_status` (
  `approval_status_id` INT(11) NOT NULL,
  `approval_status_value` VARCHAR(255) NOT NULL,
  PRIMARY KEY (`approval_status_id`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = latin1;


-- -----------------------------------------------------
-- Table `hiresmith_etl_sandbox`.`hiresmith_employer`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `hiresmith_etl_sandbox`.`hiresmith_employer` (
  `hs_employer_id` BIGINT(20) NOT NULL,
  `employer_name` VARCHAR(255) NULL DEFAULT NULL,
  `alternate_names` VARCHAR(500) NULL DEFAULT NULL,
  `do_not_merge` VARCHAR(255) NULL DEFAULT NULL,
  `sf_account_id` VARCHAR(50) NULL DEFAULT NULL,
  `link_url` VARCHAR(255) NULL DEFAULT NULL,
  `number_employees_name` VARCHAR(50) NULL DEFAULT NULL,
  `website` VARCHAR(255) NULL DEFAULT NULL,
  `account_manager_name` VARCHAR(50) NULL DEFAULT NULL,
  `outreach_lead_name` VARCHAR(50) NULL DEFAULT NULL,
  `outreach_priority_name` VARCHAR(50) NULL DEFAULT NULL,
  `outreach_status` VARCHAR(50) NULL DEFAULT NULL,
  `er_team_lead` VARCHAR(255) NULL DEFAULT NULL,
  `ed_team_lead` VARCHAR(255) NULL DEFAULT NULL,
  `employer_classification` VARCHAR(255) NULL DEFAULT NULL,
  `outreach_settings_current_as_of` DATE NULL DEFAULT NULL,
  `industries_name` VARCHAR(50) NULL DEFAULT NULL,
  `create_date` DATETIME NULL DEFAULT NULL,
  `modify_date` DATETIME NULL DEFAULT NULL,
  `parent_id` BIGINT(20) NULL DEFAULT NULL,
  `parent_company_name` VARCHAR(255) NULL DEFAULT NULL,
  `employer_city` VARCHAR(255) NULL DEFAULT NULL,
  `employer_metro_area` VARCHAR(255) NULL DEFAULT NULL,
  `employer_state` VARCHAR(255) NULL DEFAULT NULL,
  `hash` VARCHAR(500) NULL DEFAULT NULL,
  `status` VARCHAR(50) NULL DEFAULT NULL,
  `timestamp` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `LastOCIDate` DATETIME NULL,
  `LastJobPostingDATe` DATETIME NULL,
  `Last12TwentyGPSpostingDate` DATETIME NULL,
  
  PRIMARY KEY (`hs_employer_id`),
  UNIQUE INDEX `hs_link_idx` (`link_url` ASC),
  UNIQUE INDEX `sf_account_id_idx` (`sf_account_id` ASC),
  INDEX `employer_name_idx` (`employer_name` ASC))
ENGINE = InnoDB
DEFAULT CHARACTER SET = latin1;


-- -----------------------------------------------------
-- Table `hiresmith_etl_sandbox`.`hiresmith_contact`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `hiresmith_etl_sandbox`.`hiresmith_contact` (
  `hs_contact_id` BIGINT(20) NOT NULL,
  `first_name` VARCHAR(255) NULL DEFAULT NULL,
  `last_name` VARCHAR(255) NULL DEFAULT NULL,
  `link_url` VARCHAR(255) NULL DEFAULT NULL,
  `sf_contact_id` VARCHAR(50) NULL DEFAULT NULL,
  `sf_account_id` VARCHAR(50) NULL DEFAULT NULL,
  `employer_name` VARCHAR(255) NULL DEFAULT NULL,
  `hs_employer_id` BIGINT(20) NULL DEFAULT NULL,
  `create_date` DATETIME NULL DEFAULT NULL,
  `modify_date` DATETIME NULL DEFAULT NULL,
  `office_phone` VARCHAR(50) NULL DEFAULT NULL,
  `cell_phone` VARCHAR(50) NULL DEFAULT NULL,
  `email` VARCHAR(255) NULL DEFAULT NULL,
  `alternate_email` VARCHAR(255) NULL DEFAULT NULL,
  `fax` VARCHAR(50) NULL DEFAULT NULL,
  `is_alumni` TINYINT(1) NULL DEFAULT NULL,
  `job_title` VARCHAR(255) NULL DEFAULT NULL,
  `is_primary` TINYINT(1) NULL DEFAULT NULL,
  `linkedin_profile_url` VARCHAR(255) NULL DEFAULT NULL,
  `prefix_name` VARCHAR(50) NULL DEFAULT NULL,
  `preferred_name` VARCHAR(255) NULL DEFAULT NULL,
  `outreach_lead` INT(11) NULL DEFAULT NULL,
  `location_address_1` VARCHAR(255) NULL DEFAULT NULL,
  `location_address_2` VARCHAR(255) NULL DEFAULT NULL,
  `location_zip_code` VARCHAR(50) NULL DEFAULT NULL,
  `location_country_name` VARCHAR(255) NULL DEFAULT NULL,
  `location_city_name` VARCHAR(255) NULL DEFAULT NULL,
  `contact_additional_information` VARCHAR(255) NULL DEFAULT NULL,
  `contact_alt_email` VARCHAR(255) NULL DEFAULT NULL,
  `contact_alumni_grad` INT(11) NULL DEFAULT NULL,
  `contact_alumni_grad_prog_name` VARCHAR(255) NULL DEFAULT NULL,
  `contact_assigned_advisor_name` VARCHAR(255) NULL DEFAULT NULL,
  `contact_company_history` VARCHAR(255) NULL DEFAULT NULL,
  `contact_has_photo` TINYINT(1) NULL DEFAULT NULL,
  `hash` VARCHAR(32) NULL DEFAULT NULL,
  `status` VARCHAR(50) NULL DEFAULT NULL,
  `timestamp` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`hs_contact_id`),
  INDEX `contact_emp_id_idx` (`hs_employer_id` ASC),
  CONSTRAINT `const_employer_id`
    FOREIGN KEY (`hs_employer_id`)
    REFERENCES `hiresmith_etl_sandbox`.`hiresmith_employer` (`hs_employer_id`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = latin1;


-- -----------------------------------------------------
-- Table `hiresmith_etl_sandbox`.`hiresmith_contact_prefix`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `hiresmith_etl_sandbox`.`hiresmith_contact_prefix` (
  `prefix_id` INT(11) NOT NULL,
  `prefix_value` VARCHAR(255) NOT NULL,
  PRIMARY KEY (`prefix_id`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = latin1;


-- -----------------------------------------------------
-- Table `hiresmith_etl_sandbox`.`hiresmith_contact_visibility`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `hiresmith_etl_sandbox`.`hiresmith_contact_visibility` (
  `visibility_id` INT(11) NOT NULL,
  `visibility_value` VARCHAR(255) NOT NULL,
  PRIMARY KEY (`visibility_id`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = latin1;


-- -----------------------------------------------------
-- Table `hiresmith_etl_sandbox`.`hiresmith_country`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `hiresmith_etl_sandbox`.`hiresmith_country` (
  `country_id` INT(11) NOT NULL,
  `country_name` VARCHAR(255) NOT NULL,
  PRIMARY KEY (`country_id`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = latin1;


-- -----------------------------------------------------
-- Table `hiresmith_etl_sandbox`.`hiresmith_ed_team_lead`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `hiresmith_etl_sandbox`.`hiresmith_ed_team_lead` (
  `id` DOUBLE NOT NULL,
  `ed_team_lead_value` VARCHAR(255) NOT NULL,
  PRIMARY KEY (`id`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = latin1;


-- -----------------------------------------------------
-- Table `hiresmith_etl_sandbox`.`hiresmith_employer_classification`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `hiresmith_etl_sandbox`.`hiresmith_employer_classification` (
  `id` DOUBLE NOT NULL,
  `employer_classification_value` VARCHAR(255) NOT NULL,
  PRIMARY KEY (`id`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = latin1;


-- -----------------------------------------------------
-- Table `hiresmith_etl_sandbox`.`hiresmith_er_team_lead`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `hiresmith_etl_sandbox`.`hiresmith_er_team_lead` (
  `id` DOUBLE NOT NULL,
  `er_team_lead_value` VARCHAR(255) NOT NULL,
  PRIMARY KEY (`id`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = latin1;


-- -----------------------------------------------------
-- Table `hiresmith_etl_sandbox`.`hiresmith_graduation_program`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `hiresmith_etl_sandbox`.`hiresmith_graduation_program` (
  `program_id` DOUBLE NOT NULL,
  `program_value` VARCHAR(255) NOT NULL,
  PRIMARY KEY (`program_id`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = latin1;


-- -----------------------------------------------------
-- Table `hiresmith_etl_sandbox`.`hiresmith_industries`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `hiresmith_etl_sandbox`.`hiresmith_industries` (
  `industry_id` DOUBLE NOT NULL,
  `industry_name` VARCHAR(255) NOT NULL,
  PRIMARY KEY (`industry_id`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = latin1;


-- -----------------------------------------------------
-- Table `hiresmith_etl_sandbox`.`hiresmith_num_employees`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `hiresmith_etl_sandbox`.`hiresmith_num_employees` (
  `num_employees_id` INT(11) NOT NULL,
  `num_employees_value` VARCHAR(255) NOT NULL,
  PRIMARY KEY (`num_employees_id`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = latin1;


-- -----------------------------------------------------
-- Table `hiresmith_etl_sandbox`.`hiresmith_outreach_lead`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `hiresmith_etl_sandbox`.`hiresmith_outreach_lead` (
  `outreach_lead_id` DOUBLE NOT NULL,
  `outreach_lead_value` VARCHAR(255) NOT NULL,
  PRIMARY KEY (`outreach_lead_id`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = latin1;


-- -----------------------------------------------------
-- Table `hiresmith_etl_sandbox`.`hiresmith_outreach_priority`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `hiresmith_etl_sandbox`.`hiresmith_outreach_priority` (
  `outreach_id` INT(11) NOT NULL,
  `outreach_priority_value` VARCHAR(255) NOT NULL,
  PRIMARY KEY (`outreach_id`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = latin1;


-- -----------------------------------------------------
-- Table `hiresmith_etl_sandbox`.`hiresmith_outreach_status`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `hiresmith_etl_sandbox`.`hiresmith_outreach_status` (
  `id` DOUBLE NOT NULL,
  `outreach_status_value` VARCHAR(255) NOT NULL,
  PRIMARY KEY (`id`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = latin1;


-- -----------------------------------------------------
-- Table `hiresmith_etl_sandbox`.`hiresmith_salesforce_employer_ids`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `hiresmith_etl_sandbox`.`hiresmith_salesforce_employer_ids` (
  `hiresmith_id` BIGINT(20) NOT NULL,
  `salesforce_id` VARCHAR(50) NOT NULL,
  INDEX `hs_sf_ids_hs_idx` (`hiresmith_id` ASC),
  INDEX `hs_sf_ids_sf_idx` (`salesforce_id` ASC))
ENGINE = InnoDB
DEFAULT CHARACTER SET = latin1;


-- -----------------------------------------------------
-- Table `hiresmith_etl_sandbox`.`industry_lookup`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `hiresmith_etl_sandbox`.`industry_lookup` (
  `detailed_name` VARCHAR(255) NULL DEFAULT NULL,
  `detailed_id` BIGINT(20) NOT NULL,
  `consolidated_name` VARCHAR(255) NULL DEFAULT NULL,
  `consolidated_id` BIGINT(20) NULL DEFAULT NULL,
  `default_value` VARCHAR(50) NULL DEFAULT NULL,
  PRIMARY KEY (`detailed_id`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = latin1;


-- -----------------------------------------------------
-- Table `hiresmith_etl_sandbox`.`job_log`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `hiresmith_etl_sandbox`.`job_log` (
  `id` INT(11) NOT NULL AUTO_INCREMENT,
  `job_name` VARCHAR(255) NULL DEFAULT NULL,
  `source` VARCHAR(50) NULL DEFAULT NULL,
  `category` VARCHAR(50) NULL DEFAULT NULL,
  `timestamp` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `status` VARCHAR(50) NULL DEFAULT NULL,
  PRIMARY KEY (`id`),
  INDEX `job_name_idx` (`job_name` ASC))
ENGINE = InnoDB
AUTO_INCREMENT = 7
DEFAULT CHARACTER SET = latin1;


-- -----------------------------------------------------
-- Table `hiresmith_etl_sandbox`.`log_contact`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `hiresmith_etl_sandbox`.`log_contact` (
  `id` INT(11) NOT NULL AUTO_INCREMENT,
  `hs_contact_id` BIGINT(20) NULL DEFAULT NULL,
  `first_name` VARCHAR(255) NULL DEFAULT NULL,
  `last_name` VARCHAR(255) NULL DEFAULT NULL,
  `link_url` VARCHAR(255) NULL DEFAULT NULL,
  `sf_contact_id` VARCHAR(50) NULL DEFAULT NULL,
  `sf_account_id` VARCHAR(50) NULL DEFAULT NULL,
  `employer_name` VARCHAR(255) NULL DEFAULT NULL,
  `hs_employer_id` BIGINT(20) NULL DEFAULT NULL,
  `create_date` DATETIME NULL DEFAULT NULL,
  `modify_date` DATETIME NULL DEFAULT NULL,
  `office_phone` VARCHAR(50) NULL DEFAULT NULL,
  `cell_phone` VARCHAR(50) NULL DEFAULT NULL,
  `email` VARCHAR(255) NULL DEFAULT NULL,
  `alternate_email` VARCHAR(255) NULL DEFAULT NULL,
  `fax` VARCHAR(50) NULL DEFAULT NULL,
  `is_alumni` TINYINT(1) NULL DEFAULT NULL,
  `job_title` VARCHAR(255) NULL DEFAULT NULL,
  `is_primary` TINYINT(1) NULL DEFAULT NULL,
  `linkedin_profile_url` VARCHAR(255) NULL DEFAULT NULL,
  `prefix_name` VARCHAR(50) NULL DEFAULT NULL,
  `preferred_name` VARCHAR(255) NULL DEFAULT NULL,
  `outreach_lead` INT(11) NULL DEFAULT NULL,
  `location_address_1` VARCHAR(255) NULL DEFAULT NULL,
  `location_address_2` VARCHAR(255) NULL DEFAULT NULL,
  `location_zip_code` VARCHAR(50) NULL DEFAULT NULL,
  `location_country_name` VARCHAR(255) NULL DEFAULT NULL,
  `location_city_name` VARCHAR(255) NULL DEFAULT NULL,
  `contact_additional_information` VARCHAR(255) NULL DEFAULT NULL,
  `contact_alt_email` VARCHAR(255) NULL DEFAULT NULL,
  `contact_alumni_grad` INT(11) NULL DEFAULT NULL,
  `contact_alumni_grad_prog_name` VARCHAR(255) NULL DEFAULT NULL,
  `contact_assigned_advisor_name` VARCHAR(255) NULL DEFAULT NULL,
  `contact_company_history` VARCHAR(255) NULL DEFAULT NULL,
  `contact_has_photo` TINYINT(1) NULL DEFAULT NULL,
  `hash` VARCHAR(500) NULL DEFAULT NULL,
  `status` VARCHAR(50) NULL DEFAULT NULL,
  `timestamp` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `system_updated` VARCHAR(45) NULL DEFAULT NULL,
  PRIMARY KEY (`id`),
  INDEX `hs_contact_id` (`hs_contact_id` ASC),
  INDEX `sf_contact_id` (`sf_contact_id` ASC))
ENGINE = InnoDB
AUTO_INCREMENT = 2
DEFAULT CHARACTER SET = latin1;


-- -----------------------------------------------------
-- Table `hiresmith_etl_sandbox`.`log_employer`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `hiresmith_etl_sandbox`.`log_employer` (
  `id` INT(11) NOT NULL AUTO_INCREMENT,
  `hs_employer_id` BIGINT(20) NULL DEFAULT NULL,
  `employer_name` VARCHAR(255) NULL DEFAULT NULL,
  `alternate_names` VARCHAR(500) NULL DEFAULT NULL,
  `do_not_merge` VARCHAR(255) NULL DEFAULT NULL,
  `sf_account_id` VARCHAR(50) NULL DEFAULT NULL,
  `link_url` VARCHAR(255) NULL DEFAULT NULL,
  `number_employees_name` VARCHAR(50) NULL DEFAULT NULL,
  `website` VARCHAR(255) NULL DEFAULT NULL,
  `account_manager_name` VARCHAR(50) NULL DEFAULT NULL,
  `outreach_lead_name` VARCHAR(50) NULL DEFAULT NULL,
  `outreach_priority_name` VARCHAR(50) NULL DEFAULT NULL,
  `outreach_status` VARCHAR(50) NULL DEFAULT NULL,
  `er_team_lead` VARCHAR(255) NULL DEFAULT NULL,
  `ed_team_lead` VARCHAR(255) NULL DEFAULT NULL,
  `employer_classification` VARCHAR(255) NULL DEFAULT NULL,
  `outreach_settings_current_as_of` DATE NULL DEFAULT NULL,
  `industries_name` VARCHAR(50) NULL DEFAULT NULL,
  `create_date` DATETIME NULL DEFAULT NULL,
  `modify_date` DATETIME NULL DEFAULT NULL,
  `parent_id` BIGINT(20) NULL DEFAULT NULL,
  `parent_company_name` VARCHAR(255) NULL DEFAULT NULL,
  `employer_city` VARCHAR(255) NULL DEFAULT NULL,
  `employer_metro_area` VARCHAR(255) NULL DEFAULT NULL,
  `employer_state` VARCHAR(255) NULL DEFAULT NULL,
  `hash` VARCHAR(500) NULL DEFAULT NULL,
  `status` VARCHAR(50) NULL DEFAULT NULL,
  `timestamp` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `system_updated` VARCHAR(45) NULL DEFAULT NULL,
  PRIMARY KEY (`id`),
  INDEX `hs_employer_idx` (`hs_employer_id` ASC),
  INDEX `sf_account_id_idx` (`sf_account_id` ASC))
ENGINE = InnoDB
AUTO_INCREMENT = 4
DEFAULT CHARACTER SET = latin1;


-- -----------------------------------------------------
-- Table `hiresmith_etl_sandbox`.`salesforce_employer`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `hiresmith_etl_sandbox`.`salesforce_employer` (
  `hs_employer_id` BIGINT(20) NULL DEFAULT NULL,
  `employer_name` VARCHAR(255) NULL DEFAULT NULL,
  `alternate_names` VARCHAR(500) NULL DEFAULT NULL,
  `do_not_merge` VARCHAR(255) NULL DEFAULT NULL,
  `sf_account_id` VARCHAR(50) NOT NULL,
  `link_url` VARCHAR(255) NULL DEFAULT NULL,
  `number_employees_name` VARCHAR(50) NULL DEFAULT NULL,
  `website` VARCHAR(255) NULL DEFAULT NULL,
  `account_manager_name` VARCHAR(50) NULL DEFAULT NULL,
  `outreach_lead_name` VARCHAR(50) NULL DEFAULT NULL,
  `outreach_priority_name` VARCHAR(50) NULL DEFAULT NULL,
  `outreach_status` VARCHAR(50) NULL DEFAULT NULL,
  `er_team_lead` VARCHAR(255) NULL DEFAULT NULL,
  `ed_team_lead` VARCHAR(255) NULL DEFAULT NULL,
  `employer_classification` VARCHAR(255) NULL DEFAULT NULL,
  `outreach_settings_current_as_of` DATE NULL DEFAULT NULL,
  `industries_name` VARCHAR(50) NULL DEFAULT NULL,
  `create_date` DATETIME NULL DEFAULT NULL,
  `modify_date` DATETIME NULL DEFAULT NULL,
  `parent_id` BIGINT(20) NULL DEFAULT NULL,
  `parent_company_name` VARCHAR(255) NULL DEFAULT NULL,
  `employer_city` VARCHAR(255) NULL DEFAULT NULL,
  `employer_metro_area` VARCHAR(255) NULL DEFAULT NULL,
  `employer_state` VARCHAR(255) NULL DEFAULT NULL,
  `hash` VARCHAR(500) NULL DEFAULT NULL,
  `status` VARCHAR(50) NULL DEFAULT NULL,
  `timestamp` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`sf_account_id`),
  UNIQUE INDEX `sf_link_idx` (`link_url` ASC),
  UNIQUE INDEX `hs_employer_idx` (`hs_employer_id` ASC),
  INDEX `employer_name_idx` (`employer_name` ASC))
ENGINE = InnoDB
DEFAULT CHARACTER SET = latin1;


-- -----------------------------------------------------
-- Table `hiresmith_etl_sandbox`.`salesforce_contact`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `hiresmith_etl_sandbox`.`salesforce_contact` (
  `hs_contact_id` BIGINT(20) NULL DEFAULT NULL,
  `first_name` VARCHAR(255) NULL DEFAULT NULL,
  `last_name` VARCHAR(255) NULL DEFAULT NULL,
  `link_url` VARCHAR(255) NULL DEFAULT NULL,
  `sf_contact_id` VARCHAR(50) NOT NULL,
  `sf_account_id` VARCHAR(50) NULL DEFAULT NULL,
  `employer_name` VARCHAR(255) NULL DEFAULT NULL,
  `hs_employer_id` BIGINT(20) NULL DEFAULT NULL,
  `create_date` DATETIME NULL DEFAULT NULL,
  `modify_date` DATETIME NULL DEFAULT NULL,
  `office_phone` VARCHAR(50) NULL DEFAULT NULL,
  `cell_phone` VARCHAR(50) NULL DEFAULT NULL,
  `email` VARCHAR(255) NULL DEFAULT NULL,
  `alternate_email` VARCHAR(255) NULL DEFAULT NULL,
  `fax` VARCHAR(50) NULL DEFAULT NULL,
  `is_alumni` TINYINT(1) NULL DEFAULT NULL,
  `job_title` VARCHAR(255) NULL DEFAULT NULL,
  `is_primary` TINYINT(1) NULL DEFAULT NULL,
  `linkedin_profile_url` VARCHAR(255) NULL DEFAULT NULL,
  `prefix_name` VARCHAR(50) NULL DEFAULT NULL,
  `preferred_name` VARCHAR(255) NULL DEFAULT NULL,
  `outreach_lead` INT(11) NULL DEFAULT NULL,
  `location_address_1` VARCHAR(255) NULL DEFAULT NULL,
  `location_address_2` VARCHAR(255) NULL DEFAULT NULL,
  `location_zip_code` VARCHAR(50) NULL DEFAULT NULL,
  `location_country_name` VARCHAR(255) NULL DEFAULT NULL,
  `location_city_name` VARCHAR(255) NULL DEFAULT NULL,
  `contact_additional_information` VARCHAR(255) NULL DEFAULT NULL,
  `contact_alt_email` VARCHAR(255) NULL DEFAULT NULL,
  `contact_alumni_grad` INT(11) NULL DEFAULT NULL,
  `contact_alumni_grad_prog_name` VARCHAR(255) NULL DEFAULT NULL,
  `contact_assigned_advisor_name` VARCHAR(255) NULL DEFAULT NULL,
  `contact_company_history` VARCHAR(255) NULL DEFAULT NULL,
  `contact_has_photo` TINYINT(1) NULL DEFAULT NULL,
  `hash` VARCHAR(500) NULL DEFAULT NULL,
  `status` VARCHAR(50) NULL DEFAULT NULL,
  `timestamp` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`sf_contact_id`),
  INDEX `contact_emp_id_idx` (`sf_account_id` ASC),
  CONSTRAINT `sf_account_id`
    FOREIGN KEY (`sf_account_id`)
    REFERENCES `hiresmith_etl_sandbox`.`salesforce_employer` (`sf_account_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB
DEFAULT CHARACTER SET = latin1;


-- -----------------------------------------------------
-- Table `hiresmith_etl_sandbox`.`translation_lookup`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `hiresmith_etl_sandbox`.`translation_lookup` (
  `name` VARCHAR(255) NULL DEFAULT NULL,
  `hs_id` BIGINT(20) NULL DEFAULT NULL,
  `hs_value` VARCHAR(255) NULL DEFAULT NULL,
  `sf_id` VARCHAR(255) NULL DEFAULT NULL,
  `sf_value` VARCHAR(255) NULL DEFAULT NULL,
  INDEX `hs_id_idx` (`hs_id` ASC),
  INDEX `sf_id_idx` (`sf_id` ASC))
ENGINE = InnoDB
DEFAULT CHARACTER SET = latin1;


CREATE TABLE IF NOT EXISTS `hiresmith_etl_sandbox`.`hs_contact_note` (
  `employer_note_Id` BIGINT(20) NOT NULL,
  `PrimaryEntityTypeId` INT NOT NULL,
  `AssociatedEntityType1Id` INT NULL,
  `AssociatedEntity1Id` BIGINT(20) NULL,
  `AssociatedEntityType2Id` INT NULL,
  `AssociatedEntity2Id` INT NULL,
  `Text` LONGTEXT NULL,
  `Date` DATETIME NULL,
  `StudentNoteTypeId` VARCHAR(45) NULL,
  `StudentNoteTypeName` VARCHAR(45) NULL,
  `CompanyNoteTypeId` INT NULL,
  `CompanyNoteTypeName` VARCHAR(45) NULL,
  `OwnerId` VARCHAR(45) NULL,
  `OwnerName` VARCHAR(45) NULL,
  `CreatorName` VARCHAR(45) NULL,
  `FileId` VARCHAR(45) NULL,
  `FileName` VARCHAR(45) NULL,
  `VisibilityId` VARCHAR(45) NULL,
  `CampaignIds` VARCHAR(500) NULL,
  `ModifyDate` DATETIME NULL,
  `PrimaryEntityId` BIGINT(20) NOT NULL,
   `status` VARCHAR(50) NULL DEFAULT NULL,
  `timestamp` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`employer_note_Id`),
  INDEX `hs_note_contact_idx` (`PrimaryEntityId` ASC) VISIBLE,
  CONSTRAINT `fk_hs_contact_note_hiresmith_contact1`
    FOREIGN KEY (`PrimaryEntityId`)
    REFERENCES `hiresmith_etl_sandbox`.`hiresmith_contact` (`hs_contact_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB
DEFAULT CHARACTER SET = latin1;


CREATE TABLE IF NOT EXISTS `hiresmith_etl_sandbox`.`hs_employer_note` (
  `employer_note_Id` BIGINT(20) NOT NULL,
  `PrimaryEntityTypeId` INT NOT NULL,
  `PrimaryEntityId` BIGINT(20) NOT NULL,
  `AssociatedEntityType1Id` INT NULL,
  `AssociatedEntity1Id` INT NULL,
  `AssociatedEntityType2Id` INT NULL,
  `AssociatedEntity2Id` INT NULL,
  `Text` LONGTEXT NULL,
  `Date` DATETIME NULL,
  `StudentNoteTypeId` VARCHAR(45) NULL,
	`StudentNoteTypeName` VARCHAR(45) NULL,
  `CompanyNoteTypeId` INT NULL,
  `CompanyNoteTypeName` VARCHAR(45) NULL,
  `OwnerId` VARCHAR(45) NULL,
  `OwnerName` VARCHAR(45) NULL,
  `CreatorName` VARCHAR(45) NULL,
  `FileId` VARCHAR(45) NULL,
  `FileName` VARCHAR(45) NULL,
  `VisibilityId` VARCHAR(45) NULL,
  `CampaignIds` VARCHAR(500) NULL,
  `ModifyDate` DATETIME NOT NULL,
  `status` VARCHAR(50) NULL DEFAULT NULL,
  `timestamp` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`employer_note_Id`),
  INDEX `employer_note_hs_employer_idx` (`PrimaryEntityId` ASC),
  CONSTRAINT `fk_employer_note_hiresmith_employer`
    FOREIGN KEY (`PrimaryEntityId`)
    REFERENCES `hiresmith_etl_sandbox`.`hiresmith_employer` (`hs_employer_id`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = latin1;


SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;
