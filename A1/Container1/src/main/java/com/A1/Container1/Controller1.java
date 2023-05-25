package com.A1.Container1;

import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RestController;

@RestController
public class Controller1 {
    @GetMapping("/hello")
    public String hello() {
        return "Hello, World!";
    }
}
