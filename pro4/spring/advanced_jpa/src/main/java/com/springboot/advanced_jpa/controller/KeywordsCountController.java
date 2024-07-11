package com.springboot.advanced_jpa.controller;

import com.springboot.advanced_jpa.model.KeywordsCount;
import com.springboot.advanced_jpa.service.KeywordsCountService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.*;

import java.util.List;

@RestController
@RequestMapping("/keywords")
public class KeywordsCountController {
    @Autowired
    private KeywordsCountService keywordsCountService;

    @GetMapping
    public List<KeywordsCount> getAllKeywordsCounts() {
        return keywordsCountService.getAllKeywordsCounts();
    }

    @GetMapping("/{keywords}")
    public KeywordsCount getKeywordsCountByKeywords(@PathVariable String keywords) {
        return keywordsCountService.getKeywordsCountByKeywords(keywords);
    }

    @PostMapping
    public KeywordsCount createKeywordsCount(@RequestBody KeywordsCount keywordsCount) {
        return keywordsCountService.createKeywordsCount(keywordsCount);
    }

    @PutMapping("/{keywords}")
    public KeywordsCount updateKeywordsCount(@PathVariable String keywords, @RequestBody KeywordsCount keywordsCountDetails) {
        return keywordsCountService.updateKeywordsCount(keywords, keywordsCountDetails);
    }

    @DeleteMapping("/{keywords}")
    public void deleteKeywordsCount(@PathVariable String keywords) {
        keywordsCountService.deleteKeywordsCount(keywords);
    }
}
