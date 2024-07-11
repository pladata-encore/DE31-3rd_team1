package com.springboot.advanced_jpa.service;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.jdbc.core.JdbcTemplate;
import org.springframework.stereotype.Service;

import java.util.List;
import java.util.Map;

@Service
public class DynamicEntityService {

    @Autowired
    private JdbcTemplate jdbcTemplate;

    public List<Map<String, Object>> getTableData(String tableName) {
        String query = String.format("SELECT * FROM `%s`", tableName);
        return jdbcTemplate.queryForList(query);
    }
}
