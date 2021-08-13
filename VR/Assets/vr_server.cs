using System;
using System.Collections;
using System.Collections.Generic;
using System.Globalization;
using UnityEngine;
using UnityEngine.Networking;
using Valve.VR;

public class vr_server : MonoBehaviour
{
    public SteamVR_Action_Boolean freez_x, freez_y, freez_z;
    public GameObject leftcontrller;

    public bool button_y_bool;
    public SteamVR_Action_Boolean button_y;
    public SteamVR_Action_Boolean button_x;
    public manip_scr scr;
    public SteamVR_Action_Vector2 vector;
    public SteamVR_Action_Vector2 vector2;
    public MeshRenderer mesh;
    public Vector3 coords_delay;
    public float rotation_;
    [Range(1,100)]
    public int speed;
    public float multiplayer;
    public Transform freez_sphere;
    Vector3 start_pos;
    public float opened = 0;
    public float opened2 = 0;
    public SteamVR_Input_Sources handType;

    public bool is_x_freez;
    public bool is_y_freez;
    public bool is_z_freez;

    bool start_Traking;

    public GameObject LeftController;

    private void Start()
    {
        start_pos = transform.position;

        button_y.AddOnStateUpListener(TriggerUpY, handType);
        button_x.AddOnStateUpListener(TriggerUpX, handType);

        freez_x.AddOnStateUpListener(TriggerUpFreezX, handType);
        freez_x.AddOnStateDownListener(TriggerDownFreezX, handType);
        //freez_y.AddOnStateUpListener(TriggerUpFreezY, handType);
        freez_y.AddOnStateDownListener(TriggerDownFreezY, handType);
        freez_z.AddOnStateUpListener(TriggerUpFreezZ, handType);
        freez_z.AddOnStateDownListener(TriggerDownFreezZ, handType);


        StartCoroutine(PostRequest("http://192.168.0.109:5000/pos/set/vr"));
    }
    public void TriggerDownFreezY(SteamVR_Action_Boolean fromAction, SteamVR_Input_Sources fromSource)
    {
        if (is_y_freez) is_y_freez = false;
        else is_y_freez = true;
    }
    public void TriggerUpFreezZ(SteamVR_Action_Boolean fromAction, SteamVR_Input_Sources fromSource)
    {
        is_z_freez = false;
    }
    public void TriggerDownFreezZ(SteamVR_Action_Boolean fromAction, SteamVR_Input_Sources fromSource)
    {
        is_z_freez = true;
    }
    public void TriggerUpFreezX(SteamVR_Action_Boolean fromAction, SteamVR_Input_Sources fromSource)
    {
        is_x_freez = false;
    }
    public void TriggerDownFreezX(SteamVR_Action_Boolean fromAction, SteamVR_Input_Sources fromSource)
    {
        is_x_freez = true;
    }
    public void TriggerUpY(SteamVR_Action_Boolean fromAction, SteamVR_Input_Sources fromSource)
    {
        if (opened > 0) opened = 0;
        else opened = 0.8f;
    }
    public void TriggerUpX(SteamVR_Action_Boolean fromAction, SteamVR_Input_Sources fromSource)
    {
        rotation_ += 90;
        if (rotation_>360) rotation_ = 0;
    }
    void Update()
    {
        if (start_Traking) transform.position = leftcontrller.transform.position;
        if (!is_x_freez && !is_y_freez && !is_z_freez)
        {
            freez_sphere.gameObject.SetActive(false);
        }
        else start_Traking = true;

        if (is_x_freez) freez_sphere.position = new Vector3(gameObject.transform.position.x, freez_sphere.position.y, freez_sphere.position.z);
        if (is_y_freez) freez_sphere.position = new Vector3(freez_sphere.position.x, gameObject.transform.position.y, freez_sphere.position.z);
        if (is_z_freez) freez_sphere.position = new Vector3(freez_sphere.position.x, freez_sphere.position.y, gameObject.transform.position.z);

        else freez_sphere.gameObject.SetActive(true);
        opened2 += vector.axis.x * Time.deltaTime * 0.25f;
        //if (vector.axis.y * Time.deltaTime != 0) Debug.Log(vector.axis.y * Time.deltaTime);
        if (opened2 > 1) opened2 = 1;
        if (opened2 < 0) opened2 = 0;
    }
    IEnumerator PostRequest(string url)
    {
        while (true)
        {
            yield return new WaitForSeconds(0.01f);
            MyClass myObject = new MyClass();
            myObject.xyz.Add(((freez_sphere.transform.position.z * -1) + start_pos.z) * multiplayer + coords_delay.x);
            myObject.xyz.Add((freez_sphere.transform.position.x - start_pos.x) * multiplayer + coords_delay.z);
            myObject.xyz.Add((freez_sphere.transform.position.y - start_pos.y) * multiplayer + coords_delay.y);
            myObject.speed = speed;
            myObject.opened = opened;
            myObject.rotation = rotation_;
            myObject.rotation2 = opened2 * 360 + 90;
            string json = JsonUtility.ToJson(myObject);
            Debug.Log(json);

            var uwr = new UnityWebRequest(url, "POST");
            byte[] jsonToSend = new System.Text.UTF8Encoding().GetBytes(json);
            uwr.uploadHandler = (UploadHandler)new UploadHandlerRaw(jsonToSend);
            uwr.downloadHandler = (DownloadHandler)new DownloadHandlerBuffer();
            uwr.SetRequestHeader("Content-Type", "application/json");

            yield return uwr.SendWebRequest();

            if (uwr.isNetworkError)
            {
                Debug.Log("Error While Sending: " + uwr.error);
                mesh.material.color = Color.red;
            }
            else
            {
                //Debug.Log("Data: " + uwr.downloadHandler.text);
                string[] return_text = uwr.downloadHandler.text.Split(char.Parse(";"));
                if (return_text[0] == "404")
                {
                    Debug.LogError("404 server not found");
                    mesh.material.color = Color.yellow;
                }
                else if (return_text[0] == "error")
                {
                    Debug.LogError("server coord error");
                    transform.position = start_pos;
                    mesh.material.color = Color.blue;
                }
                else if (return_text[0] == "tomuch")
                {
                    Debug.LogError("tomuch coords");
                    mesh.material.color = Color.red;
                }
                else if (return_text[0] == "ok")
                {
                    string sp = NumberFormatInfo.CurrentInfo.CurrencyDecimalSeparator;
                    return_text[2] = return_text[2].Replace(".", sp);
                    float float1 = float.Parse(return_text[2]);
                    scr.alf1 = -float1 * Mathf.Rad2Deg;

                    return_text[1] = return_text[1].Replace(".", sp);
                    float1 = float.Parse(return_text[1]);
                    scr.table = -float1 * Mathf.Rad2Deg;

                    return_text[3] = return_text[3].Replace(".", sp);
                    float1 = float.Parse(return_text[3]);
                    scr.alf2 = -float1 * Mathf.Rad2Deg;

                    return_text[4] = return_text[4].Replace(".", sp);
                    float1 = float.Parse(return_text[4]);
                    scr.alf3 = opened2 * 360;
                    scr.alf4 = rotation_;
                    scr.alf3 = (opened2 * 180 + 180) - (180 - scr.alf1 - scr.alf2);
                    scr.grab_open = 40 - (opened * 40);

                    mesh.material.color = Color.green;
                }
            }
        }
    }
}
[Serializable]
public class MyClass
{
    public List<float> xyz = new List<float>();
    public int speed;
    public float rotation, rotation2;
    public float opened;
}
