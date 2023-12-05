package com.example.rolltogether.ui.home

import android.os.Bundle
import android.view.LayoutInflater
import android.view.View
import android.view.ViewGroup
import android.widget.Button
import android.widget.EditText
import android.widget.TextView
import androidx.fragment.app.Fragment
import androidx.lifecycle.ViewModelProvider
import com.example.rolltogether.R
import com.example.rolltogether.databinding.FragmentHomeBinding
import android.util.Log
import okhttp3.Call
import okhttp3.Callback
import okhttp3.MediaType.Companion.toMediaType
import okhttp3.MultipartBody
import okhttp3.OkHttpClient
import okhttp3.Request
import okhttp3.RequestBody.Companion.toRequestBody
import okhttp3.Response
import org.json.JSONObject
import java.io.IOException

class HomeFragment : Fragment() {

    private var _binding: FragmentHomeBinding? = null
    private val client = OkHttpClient()

    // This property is only valid between onCreateView and
    // onDestroyView.
    private val binding get() = _binding!!

    override fun onCreateView(
            inflater: LayoutInflater,
            container: ViewGroup?,
            savedInstanceState: Bundle?
    ): View {


        val homeViewModel =
                ViewModelProvider(this).get(HomeViewModel::class.java)

        _binding = FragmentHomeBinding.inflate(inflater, container, false)
        val root: View = binding.root

        val textView: TextView = binding.schedLabel
        homeViewModel.text.observe(viewLifecycleOwner) {
            textView.text = it
        }

        return root
    }

    override fun onViewCreated(view: View, savedInstanceState: Bundle?) {
        super.onViewCreated(view, savedInstanceState)

        view.findViewById<Button>(R.id.submitButton).setOnClickListener {
            val riderId = view.findViewById<EditText>(R.id.rider_id)
            val depCoords = view.findViewById<EditText>(R.id.departure_coords).text.split(",")
            val arrCoords = view.findViewById<EditText>(R.id.arrival_coords).text.split(",")
            val depDT = view.findViewById<EditText>(R.id.departure_date)
            val arrDT = view.findViewById<EditText>(R.id.arrival_date)
            println(riderId.text)
            println(depDT.text)
            println(arrDT.text)

            val depX = depCoords[0]
            val depY = depCoords[1]

            val arrX = arrCoords[0]
            val arrY = arrCoords[1]

//            val jsonObject = JSONObject()
//            jsonObject.put("rider_id", riderId.text)
//            jsonObject.put("departure_locX", depX)
//            jsonObject.put("departure_locY", depY)
//            jsonObject.put("arrival_locX", arrX)
//            jsonObject.put("arrival_locY", arrY)
//            jsonObject.put("departure_time", depDT.text)
//            jsonObject.put("arrival_time", arrDT.text)

//            val jsonString = jsonObject.toString()
            val mediaType = "text/plain".toMediaType()
//            val requestBody = jsonString.toRequestBody(mediaType)

            val body = MultipartBody
                .Builder()
                .setType(MultipartBody.FORM)
                .addFormDataPart("rider_id", riderId.text.toString())
                .addFormDataPart("departure_locX", depX)
                .addFormDataPart("departure_locY", depY)
                .addFormDataPart("arrival_locX", arrX)
                .addFormDataPart("arrival_locY", arrY)
                .addFormDataPart("departure_time", depDT.text.toString())
                .addFormDataPart("arrival_time", arrDT.text.toString())
                .build()

            println(riderId.text.toString())

            val request = Request.Builder()
                .url("https://roll-together-3nzis7ktnq-uc.a.run.app/api/schedules")
                .post(body)
                .build()

            val response = client.newCall(request).enqueue(object : Callback {
                override fun onFailure(call: Call, e: IOException) {
                    e.printStackTrace()
                }

                override fun onResponse(call: Call, response: Response) {
                    response.use {
                        if (!response.isSuccessful) throw IOException("Unexpected code $response")

                        val resp = response.body?.string()
                        println(resp)
                    }
                }
            })

        }

    }

    private fun requestGroups(url: String): Response {
        val client = OkHttpClient()
        val request = Request.Builder()
            .url(url)
            .build()
        return client.newCall(request).execute()
    }

    override fun onDestroyView() {
        super.onDestroyView()
        _binding = null
    }
}