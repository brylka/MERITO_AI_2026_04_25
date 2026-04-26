package com.example.myapplication;

import android.os.Bundle;
import android.widget.Button;
import android.widget.EditText;
import android.widget.TextView;
import androidx.appcompat.app.AppCompatActivity;
import org.json.JSONArray;
import org.json.JSONObject;
import java.io.BufferedReader;
import java.io.InputStreamReader;
import java.io.OutputStream;
import java.net.HttpURLConnection;
import java.net.URL;

public class MainActivity extends AppCompatActivity {

    private static final String URL_CHAT = "http://10.0.2.2:5000/api/chat";

    private JSONArray history = new JSONArray();

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        EditText prompt = findViewById(R.id.prompt);
        Button send = findViewById(R.id.send);
        TextView chat = findViewById(R.id.chat);

        send.setOnClickListener(v -> {
            String text = prompt.getText().toString();
            prompt.setText("");

            new Thread(() -> {
                try {
                    JSONObject userMsg = new JSONObject();
                    userMsg.put("role", "user");
                    JSONArray userParts = new JSONArray();
                    userParts.put(new JSONObject().put("text", text));
                    userMsg.put("parts", userParts);
                    history.put(userMsg);

                    JSONObject body = new JSONObject();
                    body.put("history", history);

                    HttpURLConnection con = (HttpURLConnection) new URL(URL_CHAT).openConnection();
                    con.setRequestMethod("POST");
                    con.setRequestProperty("Content-Type", "application/json");
                    con.setDoOutput(true);

                    OutputStream os = con.getOutputStream();
                    os.write(body.toString().getBytes("UTF-8"));
                    os.close();

                    BufferedReader br = new BufferedReader(new InputStreamReader(con.getInputStream(), "UTF-8"));
                    StringBuilder sb = new StringBuilder();
                    String line;
                    while ((line = br.readLine()) != null) sb.append(line);
                    br.close();

                    JSONObject resp = new JSONObject(sb.toString());
                    String answer = resp.getString("answer");

                    JSONObject modelMsg = new JSONObject();
                    modelMsg.put("role", "model");
                    JSONArray modelParts = new JSONArray();
                    modelParts.put(new JSONObject().put("text", answer));
                    modelMsg.put("parts", modelParts);
                    history.put(modelMsg);

                    StringBuilder out = new StringBuilder();
                    for (int i = 0; i < history.length(); i++) {
                        JSONObject m = history.getJSONObject(i);
                        String role = m.getString("role");
                        String txt = m.getJSONArray("parts").getJSONObject(0).getString("text");
                        out.append(role).append(": ").append(txt).append("\n\n");
                    }

                    runOnUiThread(() -> chat.setText(out.toString()));
                } catch (Exception e) {
                    runOnUiThread(() -> chat.setText("Błąd: " + e.getMessage()));
                }
            }).start();
        });
    }
}