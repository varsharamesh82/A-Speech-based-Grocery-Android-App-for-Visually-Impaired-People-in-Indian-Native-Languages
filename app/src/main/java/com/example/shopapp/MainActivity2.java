package com.example.shopapp;

import androidx.annotation.NonNull;
import androidx.annotation.Nullable;
import androidx.appcompat.app.AppCompatActivity;
import android.speech.tts.TextToSpeech;
import android.content.Intent;
import android.speech.RecognizerIntent;
import android.util.Log;
import android.view.View;
import android.widget.ImageButton;
import android.widget.Toast;
import android.os.Bundle;
import android.widget.TextView;

import com.chaquo.python.PyObject;
import com.chaquo.python.Python;
import com.chaquo.python.android.AndroidPlatform;

import com.chaquo.python.android.PyApplication;
import com.google.android.gms.tasks.OnFailureListener;
import com.google.android.gms.tasks.OnSuccessListener;
import com.google.mlkit.common.model.DownloadConditions;
import com.google.mlkit.nl.translate.TranslateLanguage;
import com.google.mlkit.nl.translate.Translation;
import com.google.mlkit.nl.translate.Translator;
import com.google.mlkit.nl.translate.TranslatorOptions;

import java.util.ArrayList;
import java.util.Locale;

public class MainActivity2 extends AppCompatActivity {

    TextView textView, textView2, textView3;
    ImageButton voice;

    private static final int REQUEST_CODE_SPEECH_INPUT = 1000;
    TextToSpeech textToSpeech;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main2);

        textView = findViewById(R.id.textview);
        textView2 = findViewById(R.id.textView2);
        textView3 = findViewById(R.id.textView3);
        voice = findViewById(R.id.imageButton2);

        textToSpeech = new TextToSpeech(getApplicationContext(), new TextToSpeech.OnInitListener() {
            @Override
            public void onInit(int i) {
                // if No error is found then only it will run
                if(i!=TextToSpeech.ERROR){
                    // To Choose language of speech
                    textToSpeech.setLanguage(Locale.ENGLISH);
                }
            }
        });

        voice.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {

                speechtotext();
            }
        });
    }

    private void speechtotext()
    {
        Intent intent = new Intent(RecognizerIntent.ACTION_RECOGNIZE_SPEECH);
        intent.putExtra(RecognizerIntent.EXTRA_LANGUAGE_MODEL, RecognizerIntent.LANGUAGE_MODEL_FREE_FORM);
        //for english input uncomment next two lines and comment hindi
        //intent.putExtra(RecognizerIntent.EXTRA_LANGUAGE, Locale.getDefault());
        //intent.putExtra(RecognizerIntent.EXTRA_LANGUAGE_MODEL, "Hi speak something");
        //the following lane takes hindi itself as input
        intent.putExtra(RecognizerIntent.EXTRA_LANGUAGE,"hi-IN");
        try {
            startActivityForResult(intent, REQUEST_CODE_SPEECH_INPUT);
        }
        catch(Exception e)
        {
            Toast.makeText(this,""+e.getMessage(),Toast.LENGTH_SHORT).show();
        }
    }

    @Override
    protected void onActivityResult(int requestCode, int resultCode, @Nullable Intent data) {

        super.onActivityResult(requestCode, resultCode, data);

        switch (requestCode) {
            case REQUEST_CODE_SPEECH_INPUT: {
                if (resultCode == RESULT_OK && null != data) {
                    ArrayList<String> result = data.getStringArrayListExtra(RecognizerIntent.EXTRA_RESULTS);



                    TranslatorOptions options = new TranslatorOptions.Builder()
                            .setSourceLanguage(TranslateLanguage.HINDI)
                            .setTargetLanguage(TranslateLanguage.ENGLISH)
                            .build();
                    final Translator hindiEnglishTranslator = Translation
                            .getClient(options);

                    DownloadConditions conditions = new DownloadConditions
                            .Builder()
                            .requireWifi()
                            .build();

                    hindiEnglishTranslator.downloadModelIfNeeded(conditions)
                            .addOnSuccessListener(new OnSuccessListener<Void>() {
                                @Override
                                public void onSuccess(Void aVoid) {

                                }
                            })
                            .addOnFailureListener(new OnFailureListener() {
                                @Override
                                public void onFailure(@NonNull Exception e) {

                                }
                            });

                    hindiEnglishTranslator.translate(result.get(0))
                            .addOnSuccessListener(new OnSuccessListener<String>() {
                                @Override
                                public void onSuccess(String s) {
                                    textView3.setText(s);
                                    String t = "The user said,"+textView3.getText().toString()+".Please be patient while I retrieve the items.";
                                    float pitch= (float) 1.12;
                                    float speed= (float) 1.00;
                                    textToSpeech.setPitch(pitch);
                                    textToSpeech.setSpeechRate(speed);
                                    textToSpeech.speak(t, TextToSpeech.QUEUE_FLUSH, null);

                                    if(!Python.isStarted())
                                        Python.start(new AndroidPlatform(getApplicationContext()));
                                    //this will start python
                                    //now create python instance
                                    Python py = Python.getInstance();
                                    //now create python object
                                    PyObject pyobj = py.getModule("textsegregation"); //give python script name

                                    //input string
                                    String input_text = textView3.getText().toString();
                                    PyObject obj1 = pyobj.callAttr("segregation", input_text);
                                    PyObject obj2 = pyobj.callAttr("tfidf", input_text);
                                    PyObject obj3 = pyobj.callAttr("search_query", input_text);
                                    //now set returned text to textView
                                    textView.setText(obj1.toString());
                                    textView2.setText(obj2.toString());
                                    //textView3.setText(obj3.toString());
                                }
                            })
                            .addOnFailureListener(new OnFailureListener() {
                                @Override
                                public void onFailure(@NonNull Exception e) {

                                }
                            });
                }
            }
        }


    }
}