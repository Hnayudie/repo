package com.example.myapplication

import OutputAnalyzer
import android.Manifest
import android.annotation.SuppressLint
import android.app.Activity
import android.content.Intent
import android.content.pm.PackageManager
import android.graphics.SurfaceTexture
import android.os.Bundle
import androidx.annotation.NonNull
import androidx.appcompat.widget.Toolbar
import androidx.core.app.ActivityCompat
import android.os.Handler
import android.os.Looper
import android.os.Message
import android.util.Log
import android.view.Menu
import android.view.MenuInflater
import android.view.MenuItem
import android.view.Surface
import android.view.TextureView
import android.view.View
import android.widget.EditText
import android.widget.TextView
import com.google.android.material.snackbar.Snackbar
import java.text.SimpleDateFormat
import java.util.*

class MainActivity : Activity(), ActivityCompat.OnRequestPermissionsResultCallback {

    private var analyzer: OutputAnalyzer? = null
    private var isMeasuring = false
    private val measurementStartTime: Long = 0
    private var justShared = false

    private val REQUEST_CODE_CAMERA = 0
    companion object {
        const val MESSAGE_UPDATE_REALTIME = 1
        const val MESSAGE_UPDATE_FINAL = 2
        const val MESSAGE_CAMERA_NOT_AVAILABLE = 3

        private const val MENU_INDEX_NEW_MEASUREMENT = 0
        private const val MENU_INDEX_EXPORT_RESULT = 1
        private const val MENU_INDEX_EXPORT_DETAILS = 2
    }

    enum class VIEW_STATE {
        MEASUREMENT,
        SHOW_RESULTS
    }

    private val mainHandler = @SuppressLint("HandlerLeak")
    object : Handler(Looper.getMainLooper()) {
        override fun handleMessage(msg: Message) {
            super.handleMessage(msg)

            when (msg.what) {
                MESSAGE_UPDATE_REALTIME -> {
                    findViewById<TextView>(R.id.textView).text = msg.obj.toString()
                }
                MESSAGE_UPDATE_FINAL -> {
                    findViewById<EditText>(R.id.editText).setText(msg.obj.toString())
                    val appMenu = (findViewById<Toolbar>(R.id.toolbar)).menu
                    setViewState(VIEW_STATE.SHOW_RESULTS)
                }
                MESSAGE_CAMERA_NOT_AVAILABLE -> {
                    Log.w("camera", msg.obj.toString())
                    findViewById<TextView>(R.id.textView).setText(R.string.camera_not_found)
                    analyzer?.stop()
                }
            }
        }
    }

    private val cameraService = CameraService(this, mainHandler)

    override fun onResume() {
        super.onResume()

        analyzer = OutputAnalyzer(this, findViewById(R.id.graphTextureView), mainHandler)

        val cameraTextureView = findViewById<TextureView>(R.id.textureView2)
        val previewSurfaceTexture = cameraTextureView.surfaceTexture

        if (previewSurfaceTexture != null && !justShared) {
            val previewSurface = Surface(previewSurfaceTexture)

            if (!packageManager.hasSystemFeature(PackageManager.FEATURE_CAMERA_FLASH)) {
                Snackbar.make(
                    findViewById(R.id.constraintLayout),
                    getString(R.string.noFlashWarning),
                    Snackbar.LENGTH_LONG
                ).show()
            }

            findViewById<Toolbar>(R.id.toolbar).menu.getItem(MENU_INDEX_NEW_MEASUREMENT).isVisible = false

            cameraService.start(previewSurface)
            analyzer?.measurePulse(cameraTextureView, cameraService)
        }
    }

    override fun onPause() {
        super.onPause()
        cameraService.stop()
        analyzer?.stop()
        analyzer = OutputAnalyzer(this, findViewById(R.id.graphTextureView), mainHandler)
    }

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_main)

        ActivityCompat.requestPermissions(this,
            arrayOf(Manifest.permission.CAMERA),
            REQUEST_CODE_CAMERA)
    }

    override fun onRequestPermissionsResult(requestCode: Int, permissions: Array<out String>, grantResults: IntArray) {
        if (requestCode == REQUEST_CODE_CAMERA) {
            if (grantResults.isNotEmpty() && grantResults[0] != PackageManager.PERMISSION_GRANTED) {
                Snackbar.make(
                    findViewById(R.id.constraintLayout),
                    getString(R.string.cameraPermissionRequired),
                    Snackbar.LENGTH_LONG
                ).show()
            }
        }
    }

    override fun onPrepareOptionsMenu(menu: Menu): Boolean {
        Log.i("MENU", "menu is being prepared")

        val inflater = menuInflater
        inflater.inflate(R.menu.menu, menu)

        return super.onPrepareOptionsMenu(menu)
    }

    fun setViewState(state: VIEW_STATE) {
        val appMenu = findViewById<Toolbar>(R.id.toolbar).menu
        when (state) {
            VIEW_STATE.MEASUREMENT -> {
                appMenu.getItem(MENU_INDEX_NEW_MEASUREMENT).isVisible = false
                appMenu.getItem(MENU_INDEX_EXPORT_RESULT).isVisible = false
                appMenu.getItem(MENU_INDEX_EXPORT_DETAILS).isVisible = false
                findViewById<View>(R.id.floatingActionButton).visibility = View.INVISIBLE
            }
            VIEW_STATE.SHOW_RESULTS -> {
                findViewById<View>(R.id.floatingActionButton).visibility = View.VISIBLE
                appMenu.getItem(MENU_INDEX_EXPORT_RESULT).isVisible = true
                appMenu.getItem(MENU_INDEX_EXPORT_DETAILS).isVisible = true
                appMenu.getItem(MENU_INDEX_NEW_MEASUREMENT).isVisible = true
            }
        }
    }

    fun onClickNewMeasurement(item: MenuItem) {
        onClickNewMeasurement()
    }

    fun onClickNewMeasurement(view: View) {
        onClickNewMeasurement()
    }

    fun onClickNewMeasurement() {
        analyzer = OutputAnalyzer(this, findViewById(R.id.graphTextureView), mainHandler)

        val empty = CharArray(0)
        findViewById<EditText>(R.id.editText).setText(empty, 0, 0)
        findViewById<TextView>(R.id.textView).setText(empty, 0, 0)

        setViewState(VIEW_STATE.MEASUREMENT)

        val cameraTextureView = findViewById<TextureView>(R.id.textureView2)
        val previewSurfaceTexture = cameraTextureView.surfaceTexture

        if (previewSurfaceTexture != null) {
            val previewSurface = Surface(previewSurfaceTexture)
            cameraService.start(previewSurface)
            analyzer?.measurePulse(cameraTextureView, cameraService)
        }
    }

    fun onClickExportResult(item: MenuItem) {
        val intent = getTextIntent(findViewById<TextView>(R.id.textView).text.toString())
        justShared = true
        startActivity(Intent.createChooser(intent, getString(R.string.send_output_to)))
    }

    fun onClickExportDetails(item: MenuItem) {
        val intent = getTextIntent(findViewById<EditText>(R.id.editText).text.toString())
        justShared = true
        startActivity(Intent.createChooser(intent, getString(R.string.send_output_to)))
    }

    private fun getTextIntent(intentText: String): Intent {
        val intent = Intent(Intent.ACTION_SEND)
        intent.type = "text/plain"
        intent.putExtra(
            Intent.EXTRA_SUBJECT,
            String.format(
                getString(R.string.output_header_template),
                SimpleDateFormat(
                    getString(R.string.dateFormat),
                    Locale.getDefault()
                ).format(Date())
            )
        )
        intent.putExtra(Intent.EXTRA_TEXT, intentText)
        return intent
    }
}
