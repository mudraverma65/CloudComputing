package com.A1.Container2;

import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RestController;

@RestController
public class Controller2 {
    @GetMapping("/greet")
    public String greet() {
        return "Greetings!";
    }
}
