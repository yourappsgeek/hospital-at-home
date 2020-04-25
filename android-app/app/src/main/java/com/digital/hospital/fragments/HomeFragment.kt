package com.digital.hospital.fragments

import android.app.AlertDialog
import android.content.Intent
import android.graphics.Color
import android.graphics.drawable.ColorDrawable
import android.net.Uri
import android.os.Bundle
import android.view.LayoutInflater
import android.view.View
import android.view.ViewGroup
import android.widget.TextView
import androidx.fragment.app.Fragment
import androidx.navigation.fragment.findNavController
import androidx.navigation.navOptions
import com.digital.hospital.R
import com.digital.hospital.databinding.HomeFragmentBinding


/**
 * Home Fragment used to navigate to another destinations
 */
class HomeFragment : Fragment() {

    private var _binding: HomeFragmentBinding? = null
    private val binding get() = _binding!!

    override fun onCreateView(
            inflater: LayoutInflater,
            container: ViewGroup?,
            savedInstanceState: Bundle?
    ): View? {

        _binding = HomeFragmentBinding.inflate(inflater,container,false)

        return binding.root
    }

    override fun onViewCreated(view: View, savedInstanceState: Bundle?) {
        super.onViewCreated(view, savedInstanceState)

        // Setup animation through navOptions
        val options = navOptions {
            anim {
                enter = R.anim.slide_in_right
                exit = R.anim.slide_out_left
                popEnter = R.anim.slide_in_left
                popExit = R.anim.slide_out_right
            }
        }

        binding.cvHealth.setOnClickListener {

            findNavController().navigate(R.id.frag_info, null, options)
        }

        binding.cvSymptom.setOnClickListener {

            findNavController().navigate(R.id.frag_info, null, options)
        }


        binding.cvOperator.setOnClickListener {

            findNavController().navigate(R.id.frag_contact, null, options)
        }

        binding.cvCall.setOnClickListener {

            showDialog()
        }
    }

    private fun showDialog() {
        val dialog = AlertDialog.Builder(context)
        dialog.setCancelable(true)
        val view: View = layoutInflater.inflate(R.layout.custom_dialog, null)

        dialog.setView(view)

        val call = view.findViewById(R.id.btnCall) as TextView

        dialog.create().let {

            it.window?.setBackgroundDrawable(ColorDrawable(Color.TRANSPARENT))

            call.setOnClickListener { _ ->

                makeCall()
                it.dismiss()
            }

            it.show()
        }
    }

    private fun makeCall()
    {
        val phone = "+34666777888"
        val intent = Intent(Intent.ACTION_DIAL, Uri.fromParts("tel", phone, null))
        requireActivity().startActivity(intent)
    }

    override fun onDestroyView() {
        super.onDestroyView()
        _binding = null
    }
}
