-- magictierlist.`sets` definition

CREATE TABLE `sets` (
  `id` int NOT NULL AUTO_INCREMENT,
  `code` varchar(6) DEFAULT NULL,
  `name` varchar(100) DEFAULT NULL,
  `icon_svg_uri` varchar(255) DEFAULT NULL,
  `scryfall_id` varchar(36) DEFAULT NULL,
  `released_at` datetime DEFAULT NULL,
  `scryfall_uri` varchar(255) DEFAULT NULL,
  `set_type` varchar(45) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `code_UNIQUE` (`code`),
  UNIQUE KEY `scryfall_id_UNIQUE` (`scryfall_id`)
) ENGINE=InnoDB;


-- magictierlist.cards definition

CREATE TABLE `cards` (
  `id` int NOT NULL AUTO_INCREMENT,
  `scryfall_id` varchar(36) DEFAULT NULL,
  `oracle_id` varchar(36) DEFAULT NULL,
  `name` varchar(255) DEFAULT NULL,
  `printed_name` varchar(255) DEFAULT NULL,
  `lang` varchar(5) DEFAULT NULL,
  `released_at` datetime DEFAULT NULL,
  `scryfall_uri` varchar(1000) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `mana_cost` varchar(50) DEFAULT NULL,
  `cmc` float DEFAULT NULL,
  `type_line` varchar(255) DEFAULT NULL,
  `printed_type_line` varchar(255) DEFAULT NULL,
  `oracle_text` varchar(2500) DEFAULT NULL,
  `printed_text` varchar(2500) DEFAULT NULL,
  `power` varchar(10) DEFAULT NULL,
  `toughness` varchar(10) DEFAULT NULL,
  `set_id` int NOT NULL,
  `number` int DEFAULT NULL,
  `rarity` varchar(25) DEFAULT NULL,
  `gatherer_url` varchar(255) DEFAULT NULL,
  `loyalty` varchar(5) DEFAULT NULL,
  `produced_mana` varchar(45) DEFAULT NULL,
  `other_face` varchar(36) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `id_UNIQUE` (`id`),
  UNIQUE KEY `scryfall_id_UNIQUE` (`scryfall_id`),
  KEY `card_set_id_idx` (`set_id`),
  KEY `cards_FK` (`other_face`),
  CONSTRAINT `card_set_id` FOREIGN KEY (`set_id`) REFERENCES `sets` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB;


-- magictierlist.image_uris definition

CREATE TABLE `image_uris` (
  `id` int NOT NULL AUTO_INCREMENT,
  `scryfall_id` varchar(36) NOT NULL,
  `small` varchar(255) DEFAULT NULL,
  `normal` varchar(255) DEFAULT NULL,
  `large` varchar(255) DEFAULT NULL,
  `png` varchar(255) DEFAULT NULL,
  `art_crop` varchar(255) DEFAULT NULL,
  `border_crop` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `image_uris_card_scryfall_id_idx` (`scryfall_id`),
  CONSTRAINT `image_uris_card_scryfall_id` FOREIGN KEY (`scryfall_id`) REFERENCES `cards` (`scryfall_id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB;


-- magictierlist.tierlists definition

CREATE TABLE `tierlists` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(255) DEFAULT NULL,
  `set_id` int DEFAULT NULL,
  `created_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  KEY `tierlist_set_id_idx` (`set_id`),
  CONSTRAINT `tierlist_set_id` FOREIGN KEY (`set_id`) REFERENCES `sets` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB;


-- magictierlist.cards_ratings definition

CREATE TABLE `cards_ratings` (
  `id` int NOT NULL AUTO_INCREMENT,
  `card_id` int NOT NULL,
  `tierlist_id` int NOT NULL,
  `rating` varchar(2) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `card_tierlist_unique` (`card_id`,`tierlist_id`),
  KEY `card_rating_card_id_idx` (`card_id`),
  KEY `card_rating_tierlist_id_idx` (`tierlist_id`),
  CONSTRAINT `card_rating_card_id` FOREIGN KEY (`card_id`) REFERENCES `cards` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `card_rating_tierlist_id` FOREIGN KEY (`tierlist_id`) REFERENCES `tierlists` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB;