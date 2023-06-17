package com.A1.Container2;

import org.json.JSONObject;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RestController;

import java.io.File;
import java.io.IOException;
import java.io.BufferedReader;
import java.io.FileReader;

@RestController
public class Controller2 {

    String returnResponse = null;
    @PostMapping(path = "/endpoint", consumes = "application/json")
    public String validateData(@RequestBody String response){
        try{
            JSONObject jsonObject = new JSONObject(response.toString());
            String fileName = null;
            fileName = jsonObject.getString("file").toString();
            String product = jsonObject.getString("product").toString();
            response = calculate(fileName,product);
        }catch (Exception e){
            System.out.println("Exception "+e);
        }
        return response;
    }

    public String calculate(String fileName, String productName){
        try{
            File file = new File("/app", fileName);
            BufferedReader bufferedReader = new BufferedReader(new FileReader(file));
//            BufferedReader bufferedReader = new BufferedReader(new FileReader(fileName));
            Boolean validCSV = true;
            String line;
            Integer sum=0;
            Integer lineNumber = 0;

            while((line = bufferedReader.readLine())!=null && validCSV == true){
                line = line.replaceAll("\\s", "");
                if(line.isEmpty()){
                    validCSV = false;
                }

                if(lineNumber == 0){
                    String[] headerData = line.split(",");
                    if(!headerData[0].equals("product") && !headerData[1].equals("amount")){
                        validCSV = false;
                    }
                }

//                if (lineNumber != 0) {
//                    String[] data = line.split(",");
//                    if (data.length == 2) {
//                        String product = data[0];
//                        if (product.equals(productName)) {
//                            String quantityStr = data[1];
//                            Integer quantity = Integer.valueOf(quantityStr);
//                            sum += quantity;
//                        }
//                    } else {
//                        validCSV = false;
//                    }
//                }

                if (lineNumber != 0) {
                    String[] data = line.split(",");
                    if (data.length != 2) {
                        validCSV = false;
                        break;
                    }

                    String product = data[0];
                    if (!product.equals(productName)) {
                        lineNumber++;
                        continue;
                    }

                    String quantityStr = data[1];
                    try {
                        int quantity = Integer.parseInt(quantityStr);
                        sum += quantity;
                    } catch (NumberFormatException e) {
                        validCSV = false;
                        break;
                    }
                }

                lineNumber++;
            }
            if(validCSV == false){
                returnResponse = "{\"file\": \"" + fileName + "\", \"error\": \"Input file not in CSV format.\"}";
            }
            else{
                returnResponse = "{\"file\": \"" + fileName + "\", \"sum\": \"" + sum + "\"}";
                //returnResponse = "{\"file\": \"" + fileName + "\", \"sum\": " + sum + "}";
            }
        }
        catch (Exception e){
            System.out.println("Exception:" +e);
        }
        return returnResponse;
    }
}
