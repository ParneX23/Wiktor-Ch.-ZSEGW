package com.example.dbadmin;

import com.sun.jdi.Value;
import javafx.application.Application;
import javafx.beans.value.ChangeListener;
import javafx.beans.value.ObservableValue;
import javafx.collections.ObservableList;
import javafx.event.ActionEvent;
import javafx.event.EventHandler;
import javafx.scene.Scene;
import javafx.scene.control.*;
import javafx.scene.input.MouseEvent;
import javafx.scene.layout.GridPane;
import javafx.stage.Stage;

import javax.swing.*;
import javax.xml.transform.Result;
import java.sql.*;

import java.io.IOException;
import java.util.ArrayList;
import java.util.List;

public class Main extends Application {

    public String dbName = "baza_danych";
    public String dbUser = "root";
    public String dbPass = "";
    public Connection connection;

    public void sztejtment(String sztejtment) throws SQLException {
        Statement statement = connection.createStatement();
        statement.execute(sztejtment);
    }

    @Override
    public void start(Stage stage) throws IOException {
        String url = "jdbc:mysql://localhost:3306/"+dbName;
        try {
            connection = DriverManager.getConnection(url, dbUser, dbPass);
        } catch (SQLException e){
            e.printStackTrace();
        }

        GridPane main = new GridPane();

        Button create = new Button("Create Table/Column");
        create.setPrefWidth(240);
        Button addRow = new Button("Add row");
        addRow.setPrefWidth(240);
        Button updateRow = new Button("Update row");
        updateRow.setPrefWidth(240);
        Button delete = new Button("Delete Row/Table");
        delete.setPrefWidth(240);
        Button findRow = new Button("Find Row");
        findRow.setPrefWidth(240);

        main.add(create, 0, 1);
        main.add(addRow, 0, 2);
        main.add(updateRow, 0, 3);
        main.add(delete, 0, 4);
        main.add(findRow, 0, 5);

        create.setOnMouseClicked((event) -> {
            Stage createStage = new Stage();
            GridPane createMain = new GridPane();

            ChoiceBox<String> choseBox = new ChoiceBox<String>();
            ObservableList<String> choseList = choseBox.getItems();
            choseList.addAll("Table", "Column");
            Label choseLabel = new Label("I want to create : ");
            Label tableLabel = new Label("Table name :");
            Label columnLabel = new Label("Column name :");
            Label dataTypeLabel = new Label("Data type :");
            TextField tableName = new TextField();
            TextField columnName = new TextField();
            TextField dataTypeName = new TextField();
            Button createButton = new Button("Create!");
            CheckBox autoIncrementCheckBox = new CheckBox("Auto Increment!");
            autoIncrementCheckBox.setVisible(false);
            columnName.textProperty().addListener((observable, oldValue, newValue)-> {
                if ("ID".equalsIgnoreCase(newValue.trim())){
                    autoIncrementCheckBox.setVisible(true);
                } else {
                    autoIncrementCheckBox.setSelected(false);
                    autoIncrementCheckBox.setVisible(false);
                }
            });

            createMain.add(choseLabel, 0,0);
            createMain.add(choseBox, 1,0);
            createMain.add(tableLabel, 0, 1);
            createMain.add(tableName, 1, 1);
            createMain.add(columnLabel, 0, 2);
            createMain.add(columnName, 1, 2);
            createMain.add(dataTypeLabel,0,3);
            createMain.add(dataTypeName, 1,3);
            createMain.add(createButton, 0, 4);
            createMain.add(autoIncrementCheckBox, 1, 4);

            //createMain.add(choseLabel, 0, 0);
            //createMain.add(choseBox, 1, 0);
            //createMain.add(tableLabel, 0, 1);
            //createMain.add(tableName, 1, 1);
            //createMain.add(columnLabel, 0, 2);
            //createMain.add(columnName, 1, 2);

            choseBox.setOnAction(new EventHandler<ActionEvent>() {
                @Override
                public void handle(ActionEvent actionEvent) {
                    if(choseBox.getValue() == "Column"){
                        createButton.setOnMouseClicked(new EventHandler<MouseEvent>() {
                            @Override
                            public void handle(MouseEvent mouseEvent) {
                                try {
                                    if (autoIncrementCheckBox.isSelected()){
                                        sztejtment("ALTER TABLE "+tableName.getText()+" ADD "+columnName.getText()+" "+dataTypeName.getText()+" PRIMARY KEY AUTO_INCREMENT");
                                    } else {
                                        sztejtment("ALTER TABLE "+tableName.getText()+" ADD "+columnName.getText()+" "+dataTypeName.getText());
                                    }
                                } catch (SQLException e) {
                                    throw new RuntimeException(e);
                                }
                                System.out.println("Stworzono kolumnę - "+columnName.getText()+" w tabeli "+tableName.getText()+"!");
                            }
                        });
                    } else {
                        createButton.setOnMouseClicked(new EventHandler<MouseEvent>() {
                            @Override
                            public void handle(MouseEvent mouseEvent) {
                                try {
                                    if (autoIncrementCheckBox.isSelected()){
                                        sztejtment("CREATE TABLE "+tableName.getText()+"("+columnName.getText()+" "+dataTypeName.getText()+" PRIMARY KEY AUTO_INCREMENT)");
                                    } else {
                                        sztejtment("CREATE TABLE "+tableName.getText()+"("+columnName.getText()+" "+dataTypeName.getText()+")");
                                    }
                                } catch (SQLException e) {
                                    throw new RuntimeException(e);
                                }
                                System.out.println("Stworzono Tabele - "+tableName.getText());
                            }
                        });
                    }
                }
            });

            Scene createScene = new Scene(createMain, 240, 140);
            createStage.setTitle("Create Table/Column");
            createStage.setScene(createScene);
            createStage.show();
        });

        addRow.setOnMouseClicked(new EventHandler<MouseEvent>() {
            @Override
            public void handle(MouseEvent mouseEvent) {
                Stage addRowStage = new Stage();
                GridPane addRowMain = new GridPane();
                GridPane generatedGridPane = new GridPane();

                ChoiceBox<String> choseBox = new ChoiceBox<String>();
                ObservableList<String> choseList = choseBox.getItems();
                try {
                    ResultSet rs = connection.getMetaData().getTables(connection.getCatalog(), null, "%",null);
                    while(rs.next()){
                        choseList.add(rs.getString("table_name"));
                    }
                } catch (SQLException e) {
                    throw new RuntimeException(e);
                }

                ArrayList<Label> labelArrayList = new ArrayList<>();
                ArrayList<TextField> textFieldArrayList = new ArrayList<>();
                List<String> dataTypeList = new ArrayList<String>();
                choseBox.getSelectionModel().selectedItemProperty().addListener((obs, oldV, newV) -> {
                    if(choseBox.getValue()!= null){
                        System.out.println("Wyświetlanie kolumn : "+choseBox.getValue());
                        try {
                            generatedGridPane.getChildren().clear();
                            labelArrayList.clear();
                            textFieldArrayList.clear();
                            dataTypeList.clear();
                            Statement st = connection.createStatement();
                            ResultSet rs = st.executeQuery("DESCRIBE "+choseBox.getValue());
                            while(rs.next()){
                                labelArrayList.add(new Label(rs.getString("Field")+" :"));
                                textFieldArrayList.add(new TextField());
                                dataTypeList.add(rs.getString("Type").toString());
                            }

                            for(int i=0; i<labelArrayList.size(); i++){
                                generatedGridPane.add(labelArrayList.get(i), 0 , i+2);
                                generatedGridPane.add(textFieldArrayList.get(i), 1 , i+2);
                            }
                        } catch (SQLException e) {
                            throw new RuntimeException(e);
                        }
                    }
                });

                Label choseLabel = new Label("Chose table : ");
                Button createButton = new Button("Insert!");

                createButton.setOnMouseClicked(new EventHandler<MouseEvent>() {
                    @Override
                    public void handle(MouseEvent mouseEvent) {
                        Statement st = null;
                        try {
                            st = connection.createStatement();
                            String query = "INSERT INTO "+choseBox.getValue()+" VALUES(";
                            for(int i = 0; i < textFieldArrayList.size(); i++){
                                if(i < textFieldArrayList.size()-1){
                                    if(dataTypeList.get(i).substring(0, 3).equals("var")){
                                        query = query+"'"+textFieldArrayList.get(i).getText().toString()+"', ";
                                    } else {
                                        System.out.println(dataTypeList.get(i).substring(0, 3));
                                        query = query+textFieldArrayList.get(i).getText().toString()+", ";
                                    }
                                } else {
                                    if(dataTypeList.get(i).substring(0, 3).equals("var")){
                                        query = query+"'"+textFieldArrayList.get(i).getText().toString()+"')";
                                    } else {
                                        System.out.println(dataTypeList.get(i).substring(0, 3));
                                        query = query+textFieldArrayList.get(i).getText().toString()+")";
                                    }
                                }
                            }
                            System.out.println(query);
                            st.execute(query);
                            System.out.println("Wykonano kwerendę : "+query);
                        } catch (SQLException e) {
                            throw new RuntimeException(e);
                        }
                    }
                });

                addRowMain.add(choseLabel, 0,0);
                addRowMain.add(choseBox, 1,0);
                addRowMain.add(generatedGridPane, 0,1);
                addRowMain.add(createButton,0,2);

                Scene createScene = new Scene(addRowMain, 240, 140);
                addRowStage.setTitle("Add Row");
                addRowStage.setScene(createScene);
                addRowStage.show();
            }
        });

        updateRow.setOnMouseClicked(new EventHandler<MouseEvent>() {
            @Override
            public void handle(MouseEvent mouseEvent) {
                Stage updateRowStage = new Stage();
                GridPane updateMain = new GridPane();
                GridPane generatedGridPane = new GridPane();

                ChoiceBox<String> choseBox = new ChoiceBox<String>();
                ObservableList<String> choseList = choseBox.getItems();
                try {
                    ResultSet rs = connection.getMetaData().getTables(connection.getCatalog(), null, "%",null);
                    while(rs.next()){
                        choseList.add(rs.getString("table_name"));
                    }
                } catch (SQLException e) {
                    throw new RuntimeException(e);
                }

                ArrayList<Label> labelArrayList = new ArrayList<>();
                ArrayList<TextField> textFieldArrayList = new ArrayList<>();
                List<String> dataTypeList = new ArrayList<String>();
                List<String> collumnNameList = new ArrayList<String>();
                choseBox.getSelectionModel().selectedItemProperty().addListener((obs, oldV, newV) -> {
                    if(choseBox.getValue()!= null){
                        System.out.println("Wyświetlanie kolumn : "+choseBox.getValue());
                        try {
                            generatedGridPane.getChildren().clear();
                            labelArrayList.clear();
                            textFieldArrayList.clear();
                            dataTypeList.clear();
                            Statement st = connection.createStatement();
                            ResultSet rs = st.executeQuery("DESCRIBE "+choseBox.getValue());
                            while(rs.next()){
                                labelArrayList.add(new Label(rs.getString("Field")+" :"));
                                textFieldArrayList.add(new TextField());
                                dataTypeList.add(rs.getString("Type").toString());
                                collumnNameList.add(rs.getString("Field").toString());
                            }

                            for(int i=0; i<labelArrayList.size(); i++){
                                generatedGridPane.add(labelArrayList.get(i), 0 , i+2);
                                generatedGridPane.add(textFieldArrayList.get(i), 1 , i+2);
                            }
                            textFieldArrayList.getFirst().textProperty().addListener((observable, oldValue, newValue)-> {
                                try {
                                    String query = "SELECT * FROM "+choseBox.getValue()+" WHERE id="+newValue.trim();
                                    System.out.println(query);
                                    Statement st2 = connection.createStatement();
                                    ResultSet rs2 = st2.executeQuery(query);
                                    while(rs2.next()){
                                        for(int i=0; i<collumnNameList.size(); i++){
                                            if(!collumnNameList.get(i).equals("id")){
                                                System.out.println(collumnNameList.get(i));
                                                textFieldArrayList.get(i).setText(rs2.getString(collumnNameList.get(i)));
                                            }
                                        }
                                    }
                                } catch (SQLException e) {
                                    throw new RuntimeException(e);
                                }
                            });

                        } catch (SQLException e) {
                            throw new RuntimeException(e);
                        }
                    }
                });

                Label choseLabel = new Label("Chose table : ");
                Button updateButton = new Button("Update!");

                updateButton.setOnMouseClicked(new EventHandler<MouseEvent>() {
                    @Override
                    public void handle(MouseEvent mouseEvent) {
                        Statement st = null;
                        try {
                            st = connection.createStatement();
                            String query = "UPDATE "+choseBox.getValue()+" SET ";
                            for(int i = 0; i < textFieldArrayList.size(); i++){
                                if(i < textFieldArrayList.size()-1){
                                    if(dataTypeList.get(i).substring(0, 3).equals("var")){
                                        query = query+collumnNameList.get(i)+" = '"+textFieldArrayList.get(i).getText().toString()+"', ";
                                    } else {
                                        System.out.println(dataTypeList.get(i).substring(0, 3));
                                        query = query+collumnNameList.get(i)+" = "+textFieldArrayList.get(i).getText().toString()+", ";
                                    }
                                } else {
                                    if(dataTypeList.get(i).substring(0, 3).equals("var")){
                                        query = query+collumnNameList.get(i)+" = '"+textFieldArrayList.get(i).getText().toString()+"'";
                                    } else {
                                        System.out.println(dataTypeList.get(i).substring(0, 3));
                                        query = query+collumnNameList.get(i)+" = "+textFieldArrayList.get(i).getText().toString();
                                    }
                                }
                            }
                            query = query+" WHERE id = "+textFieldArrayList.get(0).getText();
                            System.out.println(query);
                            st.execute(query);
                            System.out.println("Wykonano kwerendę : "+query);
                        } catch (SQLException e) {
                            throw new RuntimeException(e);
                        }
                    }
                });

                updateMain.add(choseLabel, 0,0);
                updateMain.add(choseBox, 1,0);
                updateMain.add(generatedGridPane, 0,1);
                updateMain.add(updateButton,0,2);

                Scene createScene = new Scene(updateMain, 240, 140);
                updateRowStage.setTitle("Update Row");
                updateRowStage.setScene(createScene);
                updateRowStage.show();
            }
        });

        delete.setOnMouseClicked(new EventHandler<MouseEvent>() {
            @Override
            public void handle(MouseEvent mouseEvent) {
                Stage deleteStage = new Stage();
                GridPane deleteMain = new GridPane();
                GridPane generatedGridPane = new GridPane();

                ChoiceBox<String> choseBox2 = new ChoiceBox<String>();
                ObservableList<String> choseList2 = choseBox2.getItems();
                choseList2.addAll("Table", "Row");
                Label choseLabel2 = new Label("I want to delete : ");

                Label choseLabel = new Label("Chose table : ");
                Button deleteButton = new Button("Delete!");

                ChoiceBox<String> choseBox = new ChoiceBox<String>();
                ObservableList<String> choseList = choseBox.getItems();
                try {
                    ResultSet rs = connection.getMetaData().getTables(connection.getCatalog(), null, "%",null);
                    while(rs.next()){
                        choseList.add(rs.getString("table_name"));
                    }
                } catch (SQLException e) {
                    throw new RuntimeException(e);
                }

                ArrayList<Label> labelArrayList = new ArrayList<>();
                ArrayList<TextField> textFieldArrayList = new ArrayList<>();
                List<String> dataTypeList = new ArrayList<String>();
                List<String> collumnNameList = new ArrayList<String>();
                choseBox.getSelectionModel().selectedItemProperty().addListener((obs2, oldVa, newVa) -> {
                    if(choseBox.getValue()!= null){
                        System.out.println("Wyświetlanie kolumn : "+choseBox.getValue());
                        try {
                            generatedGridPane.getChildren().clear();
                            labelArrayList.clear();
                            textFieldArrayList.clear();
                            dataTypeList.clear();
                            Statement st = connection.createStatement();
                            ResultSet rs = st.executeQuery("DESCRIBE "+choseBox.getValue());
                            while(rs.next()){
                                labelArrayList.add(new Label(rs.getString("Field")+" :"));
                                textFieldArrayList.add(new TextField());
                                dataTypeList.add(rs.getString("Type").toString());
                                collumnNameList.add(rs.getString("Field").toString());
                            }

                            for(int i=0; i<labelArrayList.size(); i++){
                                generatedGridPane.add(labelArrayList.get(i), 0 , i+2);
                                generatedGridPane.add(textFieldArrayList.get(i), 1 , i+2);
                            }

                        } catch (SQLException e) {
                            throw new RuntimeException(e);
                        }
                    }
                });

                deleteButton.setOnMouseClicked(new EventHandler<MouseEvent>() {
                    @Override
                    public void handle(MouseEvent mouseEvent) {
                        if(choseBox2.getValue()=="Row"){
                                    Statement st = null;

                                    try {
                                        st = connection.createStatement();
                                        String query = "DELETE FROM "+choseBox.getValue()+" WHERE ";
                                        for(int i = 0; i < textFieldArrayList.size(); i++){
                                            String field = textFieldArrayList.get(i).getText();
                                            if(field==""){
                                                textFieldArrayList.get(i).setText("null");
                                            }
                                            if(i < textFieldArrayList.size()-1){
                                                if(dataTypeList.get(i).substring(0, 3).equals("var")){
                                                    query = query+collumnNameList.get(i)+" = '"+textFieldArrayList.get(i).getText().toString()+"' OR";
                                                } else {
                                                    System.out.println(dataTypeList.get(i).substring(0, 3));
                                                    query = query+collumnNameList.get(i)+" = "+textFieldArrayList.get(i).getText().toString()+" OR ";
                                                }
                                            } else {
                                                if(dataTypeList.get(i).substring(0, 3).equals("var")){
                                                    query = query+collumnNameList.get(i)+" = '"+textFieldArrayList.get(i).getText().toString()+"'";
                                                } else {
                                                    System.out.println(dataTypeList.get(i).substring(0, 3));
                                                    query = query+collumnNameList.get(i)+" = "+textFieldArrayList.get(i).getText().toString();
                                                }
                                            }
                                        }
                                        System.out.println(query);
                                        st.execute(query);
                                        System.out.println("Wykonano kwerendę : "+query);
                                    } catch (SQLException e) {
                                        throw new RuntimeException(e);
                                    }
                        } else {
                                    Statement st = null;

                                    try {
                                        st = connection.createStatement();
                                        String query = "DROP TABLE "+choseBox.getValue();
                                        System.out.println(query);
                                        st.execute(query);
                                        System.out.println("Wykonano kwerendę : "+query);
                                    } catch (SQLException e) {
                                        throw new RuntimeException(e);
                                    }
                        }
                    }
                });

                deleteMain.add(choseLabel2, 0,0);
                deleteMain.add(choseBox2, 1,0);
                deleteMain.add(choseLabel, 0,1);
                deleteMain.add(choseBox, 1,1);
                deleteMain.add(generatedGridPane, 0,2);
                deleteMain.add(deleteButton,0,3);

                Scene createScene = new Scene(deleteMain, 240, 140);
                deleteStage.setTitle("Delete");
                deleteStage.setScene(createScene);
                deleteStage.show();
            }
        });

        findRow.setOnMouseClicked(new EventHandler<MouseEvent>() {
            @Override
            public void handle(MouseEvent mouseEvent) {
                Stage findStage = new Stage();
                GridPane findMain = new GridPane();
                GridPane generatedGridPane = new GridPane();

                ChoiceBox<String> choseBox = new ChoiceBox<String>();
                ObservableList<String> choseList = choseBox.getItems();
                try {
                    ResultSet rs = connection.getMetaData().getTables(connection.getCatalog(), null, "%",null);
                    while(rs.next()){
                        choseList.add(rs.getString("table_name"));
                    }
                } catch (SQLException e) {
                    throw new RuntimeException(e);
                }

                ArrayList<Label> labelArrayList = new ArrayList<>();
                ArrayList<TextField> textFieldArrayList = new ArrayList<>();
                List<String> dataTypeList = new ArrayList<String>();
                List<String> collumnNameList = new ArrayList<String>();
                choseBox.getSelectionModel().selectedItemProperty().addListener((obs, oldV, newV) -> {
                    if(choseBox.getValue()!= null){
                        System.out.println("Wyświetlanie kolumn : "+choseBox.getValue());
                        try {
                            generatedGridPane.getChildren().clear();
                            labelArrayList.clear();
                            textFieldArrayList.clear();
                            dataTypeList.clear();
                            Statement st = connection.createStatement();
                            ResultSet rs = st.executeQuery("DESCRIBE "+choseBox.getValue());
                            while(rs.next()){
                                labelArrayList.add(new Label(rs.getString("Field")+" :"));
                                textFieldArrayList.add(new TextField());
                                dataTypeList.add(rs.getString("Type").toString());
                                collumnNameList.add(rs.getString("Field").toString());
                            }

                            for(int i=0; i<labelArrayList.size(); i++){
                                generatedGridPane.add(labelArrayList.get(i), 0 , i+2);
                                generatedGridPane.add(textFieldArrayList.get(i), 1 , i+2);
                            }
                        } catch (SQLException e) {
                            throw new RuntimeException(e);
                        }
                    }
                });

                Label choseLabel = new Label("Chose table : ");
                Button findButton = new Button("Find!");

                findButton.setOnMouseClicked(new EventHandler<MouseEvent>() {
                    @Override
                    public void handle(MouseEvent mouseEvent) {
                        try {
                            String query = "SELECT * FROM "+choseBox.getValue()+" WHERE ";
                            boolean didItStarter = false;
                            for(int i = 0; i < textFieldArrayList.size(); i++){
                                if(!didItStarter && !textFieldArrayList.get(i).getText().equals("")){
                                    if(dataTypeList.get(i).substring(0, 3).equals("var")){
                                        query = query+collumnNameList.get(i)+" = '"+textFieldArrayList.get(i).getText().toString()+"'";
                                        didItStarter = true;
                                    } else {
                                        System.out.println(dataTypeList.get(i).substring(0, 3));
                                        query = query+collumnNameList.get(i)+" = "+textFieldArrayList.get(i).getText().toString();
                                        didItStarter = true;
                                    }
                                } else if (!textFieldArrayList.get(i).getText().equals("")){
                                    if(dataTypeList.get(i).substring(0, 3).equals("var")){
                                        query = query+" OR "+collumnNameList.get(i)+" = '"+textFieldArrayList.get(i).getText().toString()+"'";
                                        didItStarter = true;
                                    } else {
                                        System.out.println(dataTypeList.get(i).substring(0, 3));
                                        query = query+" OR "+collumnNameList.get(i)+" = "+textFieldArrayList.get(i).getText().toString();
                                        didItStarter = true;
                                    }
                                }
                            }
                            System.out.println(query);
                                Statement st2 = connection.createStatement();
                                ResultSet rs2 = st2.executeQuery(query);
                                while(rs2.next()){
                                    for(int i=0; i<collumnNameList.size(); i++){
                                        System.out.println(collumnNameList.get(i));
                                        textFieldArrayList.get(i).setText(rs2.getString(collumnNameList.get(i)));
                                    }
                                }
                        } catch (SQLException e) {
                            throw new RuntimeException(e);
                        }
                    }
                });

                findMain.add(choseLabel, 0,0);
                findMain.add(choseBox, 1,0);
                findMain.add(generatedGridPane, 0,1);
                findMain.add(findButton,0,2);

                Scene createScene = new Scene(findMain, 240, 140);
                findStage.setTitle("Find Row");
                findStage.setScene(createScene);
                findStage.show();
            }
        });

        Scene scene = new Scene(main, 240, 130);
        stage.setTitle("DBAdmin");
        stage.setScene(scene);
        stage.show();
    }



    public static void main(String[] args) {
        launch();
    }
}