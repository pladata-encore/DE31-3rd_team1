package com.springboot.advanced_jpa.repository;

import com.springboot.advanced_jpa.model.KeywordsCount;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

import java.util.Optional;

@Repository
public interface KeywordsCountRepository extends JpaRepository<KeywordsCount, Long> {
    Optional<KeywordsCount> findByKeywords(String keywords);
    void deleteByKeywords(String keywords);
}
