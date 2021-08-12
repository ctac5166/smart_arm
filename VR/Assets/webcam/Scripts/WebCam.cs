using UnityEngine;
using System.Collections;
using UnityEngine.UI;

public class WebCam : MonoBehaviour
{
    int currentCamIndex = 0;

    WebCamTexture tex;

    public RawImage display;
    public RawImage display2;

    public Text startStopText;

    public Text debug;
    private void Start()
    {
        StartStopCam_Clicked();
    }
    public void SwapCam_Clicked()
    {
        if (WebCamTexture.devices.Length > 0)
        {
            currentCamIndex += 1;
            currentCamIndex %= WebCamTexture.devices.Length;

            // if tex is not null:
            // stop the web cam
            // start the web cam

            if (tex != null)
            {
                StopWebCam();
                StartStopCam_Clicked();
            }
        }
    }

    public void StartStopCam_Clicked()
    {
        if (tex != null) // Stop the camera
        {
            StopWebCam();
            startStopText.text = "Start Camera";
        }
        else // Start the camera
        {
            WebCamDevice device = WebCamTexture.devices[1];
            tex = new WebCamTexture(device.name);
            display.texture = tex;

            tex.Play();

            WebCamDevice device2 = WebCamTexture.devices[0];
            tex = new WebCamTexture(device2.name);
            display2.texture = tex;

            tex.Play();

            startStopText.text = "Stop Camera";
        }
    }

    private void StopWebCam()
    {
        display.texture = null;
        tex.Stop();
        tex = null;
    }
}
