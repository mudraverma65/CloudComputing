package com.A1.Container2;

import org.json.JSONObject;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RestController;

import java.io.BufferedReader;
import java.io.FileReader;

@RestController
public class Controller2 {

    JSONObject returnJson = new JSONObject();

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
            BufferedReader bufferedReader = new BufferedReader(new FileReader("/app/"+fileName));
            Boolean validCSV = true;
            String line;
            Integer sum=0;
            Integer lineNumber = 0;

            while((line = bufferedReader.readLine())!=null && validCSV == true){
                if(line.isEmpty()){
                    validCSV = false;
                }

                if(lineNumber == 0){
                    String[] headerData = line.split(",");
                    if(!headerData[0].equals("product") && !headerData[1].equals("amount")){
                        validCSV = false;
                    }
                }

                if (lineNumber != 0) {
                    String[] data = line.split(",");
                    if (data.length == 2) {
                        String product = data[0];
                        if (product.equals(productName)) {
                            Integer quantity = Integer.valueOf(data[1]);
                            sum += quantity;
                        }
                    } else {
                        validCSV = false;
                    }
                }
                lineNumber++;
            }
            if(validCSV == false){
                returnResponse = "{\"file\": \"" + fileName + "\", \"error\": \"Input file not in CSV format.\"}";
            }
            else{
                returnResponse = "{\"file\": \"" + fileName + "\", \"sum\": " + sum + "}";
            }
        }
        catch (Exception e){
            System.out.println("Exception:" +e);
        }
        return returnResponse;
    }
}
