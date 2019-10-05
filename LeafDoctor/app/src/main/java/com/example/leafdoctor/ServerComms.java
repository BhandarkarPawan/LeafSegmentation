package com.example.leafdoctor;

import android.os.AsyncTask;
import android.util.Log;

import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.io.PrintWriter;
import java.net.Socket;
import java.net.UnknownHostException;

public class ServerComms extends AsyncTask<String, Void, String> {

    Socket server;
    PrintWriter printwriter;
    BufferedReader in;
    int HEADER_SIZE = 10;
    final String LOG_TAG = "SERVER COMMS: ";
    @Override
    protected String doInBackground(String... params) {
        try {


            Log.v(LOG_TAG, "Doing in background!");

            String message = params[0];

            String header = String.format("%10s", message.length());
            message = header + message;

            server = new Socket("192.168.0.107", 1234);  //connect to server
            printwriter = new PrintWriter(server.getOutputStream(), true);
            printwriter.write(message);  //write the message to output stream
            printwriter.flush();

            in = new BufferedReader(new InputStreamReader(server.getInputStream()));

            Log.v(LOG_TAG, "About to read");

            String response = in.readLine();
            Log.v(LOG_TAG,"Read Success: " +  response);

            Log.v(LOG_TAG, response.equals("Success") + "");

            if(response.equals("Success"))
                MainActivity.fetch_mask();

            server.close();
            printwriter.close();




        } catch (UnknownHostException e) {
            e.printStackTrace();
            return "Host Unknown";
        } catch (IOException e) {
            e.printStackTrace();
            return "Connection Failed";
        }
        return "Executed";

    }

}
