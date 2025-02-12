package com.example.ziptofile;

import javafx.application.Application;
import javafx.event.EventHandler;
import javafx.scene.Scene;
import javafx.scene.control.Button;
import javafx.scene.control.Label;
import javafx.scene.control.TextField;
import javafx.scene.input.MouseEvent;
import javafx.scene.layout.GridPane;
import javafx.scene.text.Text;
import javafx.stage.FileChooser;
import javafx.stage.Stage;

import java.io.*;
import java.util.Scanner;
import java.util.zip.ZipEntry;
import java.util.zip.ZipInputStream;
import java.util.zip.ZipOutputStream;

import static javafx.application.Application.launch;

public class Main extends Application {
    public static void main(String[] args) throws IOException {
        HelloApplication.launch();
        //ZipOutputStream, ZipEntry, ZipInputStream
        System.out.println("1. Dokonaj kompresji pliku.");
        System.out.println("2. Dokonaj dekompresji pliku.");
        System.out.println("3. Wyjście");
        int n = getInt();

        //if (n == 1) fileToZip();
        //else if(n == 2) zipDecompressor();
       // else System.exit(0);

    }

    public static void zipDecompressor(String fileZip, String destDir) throws IOException {

        byte[] buffer = new byte[1024];
        ZipInputStream zis = new ZipInputStream(new FileInputStream(fileZip));
        ZipEntry zipEntry = zis.getNextEntry();

        while (zipEntry != null) {
            File newFile = new File(destDir + File.separator + zipEntry.getName());
            new File(newFile.getParent()).mkdirs();
            FileOutputStream fos = new FileOutputStream(newFile);
            int len;
            while ((len = zis.read(buffer)) > 0) {
                fos.write(buffer, 0, len);
            }
            fos.close();
            zipEntry = zis.getNextEntry();
        }
        zis.closeEntry();
        zis.close();

        System.out.println("Plik zdekompresowany do folderu: " + destDir);

    }

    public static int getInt() {
        return new Scanner(System.in).nextInt();
    }

    @Override
    public void start(Stage stage) throws Exception {
        GridPane main = new GridPane();

        Label label1 = new Label("Wybierz folder z plikami do spakowania");
        Label label2 = new Label("Wybierz folder gdzie zostanie umieszczone archiwum");
        Button zipBtn = new Button("Spakuj");
        TextField filesPath = new TextField();
        TextField zipPath = new TextField();

        Label label3 = new Label("Wybierz archiwum z plikami do rozpakowania");
        Label label4 = new Label("Wybierz folder gdzie zostaną rozpakowane pliki");
        Button unzipBtn = new Button("Rozpakuj");
        TextField filesPath2 = new TextField();
        TextField unzipPath = new TextField();

        main.add(label1, 0 ,0);
        main.add(filesPath, 1 ,0);
        main.add(label2, 0 ,1);
        main.add(zipPath, 1 ,1);
        main.add(zipBtn, 0, 2);
        main.add(label3, 0 ,3);
        main.add(filesPath2, 1 ,3);
        main.add(label4, 0 ,4);
        main.add(unzipPath, 1 ,4);
        main.add(unzipBtn, 0, 5);

        zipBtn.setOnMouseClicked(new EventHandler<MouseEvent>() {
            @Override
            public void handle(MouseEvent mouseEvent) {
                try {
                    Main.fileToZip(filesPath.getText(), zipPath.getText());
                } catch (IOException e) {
                    throw new RuntimeException(e);
                }
            }
        });
        unzipBtn.setOnMouseClicked(new EventHandler<MouseEvent>() {
            @Override
            public void handle(MouseEvent mouseEvent) {
                try {
                    Main.zipDecompressor(filesPath2.getText(), unzipPath.getText());
                } catch (IOException e) {
                    throw new RuntimeException(e);
                }
            }
        });

        Scene scene = new Scene(main, 320, 240);
        stage.setTitle("ZipToFile");
        stage.setScene(scene);
        stage.show();
    }


    public static void fileToZip(String sourceFile, String zipFileName) throws IOException {
        FileOutputStream fos = new FileOutputStream(zipFileName);
        ZipOutputStream zipOut = new ZipOutputStream(fos);
        File fileToZip = new File(sourceFile);

        FileInputStream fis = new FileInputStream(fileToZip);
        ZipEntry zipEntry = new ZipEntry(fileToZip.getName());
        zipOut.putNextEntry(zipEntry);

        byte[] bytes = new byte[1024];
        int length;
        while ((length = fis.read(bytes)) >= 0) {
            zipOut.write(bytes, 0, length);
        }
        fis.close();
        zipOut.close();
        fos.close();

        System.out.println("Plik skompresowany do: " + zipFileName);
    }
}