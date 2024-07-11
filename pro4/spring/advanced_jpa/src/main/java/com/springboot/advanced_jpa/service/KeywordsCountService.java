package com.springboot.advanced_jpa.service;

import com.springboot.advanced_jpa.model.KeywordsCount;
import com.springboot.advanced_jpa.repository.KeywordsCountRepository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import java.util.List;

@Service
public class KeywordsCountService {
    @Autowired
    private KeywordsCountRepository keywordsCountRepository;

    public List<KeywordsCount> getAllKeywordsCounts() {
        return keywordsCountRepository.findAll();
    }

    public KeywordsCount getKeywordsCountByKeywords(String keywords) {
        return keywordsCountRepository.findByKeywords(keywords).orElse(null);
    }

    public KeywordsCount createKeywordsCount(KeywordsCount keywordsCount) {
        return keywordsCountRepository.save(keywordsCount);
    }

    public KeywordsCount updateKeywordsCount(String keywords, KeywordsCount keywordsCountDetails) {
        KeywordsCount keywordsCount = keywordsCountRepository.findByKeywords(keywords).orElse(null);
        if (keywordsCount != null) {
            keywordsCount.setCount(keywordsCountDetails.getCount());
            return keywordsCountRepository.save(keywordsCount);
        }
        return null;
    }

    public void deleteKeywordsCount(String keywords) {
        keywordsCountRepository.deleteByKeywords(keywords);
    }
}
