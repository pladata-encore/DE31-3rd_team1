package com.springboot.advanced_jpa.controller;

import com.springboot.advanced_jpa.service.DynamicEntityService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.*;

import java.util.List;
import java.util.Map;

@RestController
@RequestMapping("/dynamic/table")
public class DynamicEntityController {

    @Autowired
    private DynamicEntityService dynamicEntityService;

    @GetMapping("/{tableName}")
    public List<Map<String, Object>> getTableData(@PathVariable String tableName) {
        return dynamicEntityService.getTableData(tableName);
    }
}
