package com.example.rolltogether.ui.notifications

import android.os.Bundle
import android.view.LayoutInflater
import android.view.View
import android.view.ViewGroup
import android.widget.TextView
import android.widget.Button
import android.widget.EditText
import androidx.fragment.app.Fragment
import androidx.lifecycle.ViewModelProvider
import com.example.rolltogether.databinding.FragmentNotificationsBinding
import com.example.rolltogether.R
import okhttp3.*
import org.json.JSONObject
import java.io.IOException


class NotificationsFragment : Fragment() {

    private var _binding: FragmentNotificationsBinding? = null
    private val client = OkHttpClient()

    // This property is only valid between onCreateView and
    // onDestroyView.
    private val binding get() = _binding!!

    override fun onCreateView(
            inflater: LayoutInflater,
            container: ViewGroup?,
            savedInstanceState: Bundle?
    ): View {
        val notificationsViewModel =
                ViewModelProvider(this).get(NotificationsViewModel::class.java)

        _binding = FragmentNotificationsBinding.inflate(inflater, container, false)
        val root: View = binding.root

//        val textView: TextView = binding.riderCreate
//        notificationsViewModel.text.observe(viewLifecycleOwner) {
//            textView.text = it
//        }
        return root
    }

    override fun onViewCreated(view: View, savedInstanceState: Bundle?) {
        super.onViewCreated(view, savedInstanceState)

        view.findViewById<Button>(R.id.createRiderButton).setOnClickListener {
            val riderFirstName = view.findViewById<EditText>(R.id.first_name)
            val riderLastInitial = view.findViewById<EditText>(R.id.last_initial)
            val riderPhoneNum = view.findViewById<EditText>(R.id.phone_num)

            val body = MultipartBody
                .Builder()
                .setType(MultipartBody.FORM)
                .addFormDataPart("first_name", riderFirstName.text.toString())
                .addFormDataPart("last_initial", riderLastInitial.text.toString())
                .addFormDataPart("phone_num", riderPhoneNum.text.toString())
                .build()

            val request = Request.Builder()
                .url("https://roll-together-3nzis7ktnq-uc.a.run.app/api/riders")
                .post(body)
                .build()

            client.newCall(request).enqueue(object : Callback {
                override fun onFailure(call: Call, e: IOException) {
                    e.printStackTrace()
                }

                override fun onResponse(call: Call, response: Response) {
                    response.use {
                        if (!response.isSuccessful) throw IOException("Unexpected code $response")

                        val resp = response.body?.string()
                        println(resp)

                        val jsonResp = JSONObject(resp)

                        var lab = view.findViewById<TextView>(R.id.riderCreate)

                        lab.text = jsonResp.get("rider_id").toString()
                    }
                }
            })
        }
    }

    override fun onDestroyView() {
        super.onDestroyView()
        _binding = null
    }
}