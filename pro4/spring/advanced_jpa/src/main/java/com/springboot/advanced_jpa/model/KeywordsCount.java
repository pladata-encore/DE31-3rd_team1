package com.springboot.advanced_jpa.model;

import lombok.Getter;
import lombok.Setter;

import jakarta.persistence.Column;
import jakarta.persistence.Entity;
import jakarta.persistence.Id;
import jakarta.persistence.Table;

@Getter
@Setter
@Entity
@Table(name = "2024-07-01")
public class KeywordsCount {

    @Id
    @Column(name = "Keyword")
    private String keywords;

    @Column(name = "count")
    private Long count;
}
