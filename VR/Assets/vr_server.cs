using System;
using System.Collections;
using System.Collections.Generic;
using System.Globalization;
using UnityEngine;
using UnityEngine.Networking;
using Valve.VR;

public class vr_server : MonoBehaviour
{
    public bool button_y_bool;
    public SteamVR_Action_Boolean button_y;
    public manip_scr scr;
    public SteamVR_Action_Vector2 vector;
    public SteamVR_Action_Vector2 vector2;
    public MeshRenderer mesh;
    public Vector3 coords_delay;
    [Range(1,100)]
    public int speed;
    public float multiplayer;
    public GameObject[] parts;
    Vector3 start_pos;
    public float opened = 0;
    public float opened2 = 0;
    private void Start()
    {
        start_pos = transform.position;
        StartCoroutine(PostRequest("http://192.168.0.109:5000/pos/set/vr"));
    }
    void Update()
    {
       // Debug.Log(transform.rotation.eulerAngles.z);
        button_y_bool = button_y.active;
        opened += vector.axis.x * Time.deltaTime;
        //if(vector.axis.x * Time.deltaTime != 0) Debug.Log(vector.axis.x * Time.deltaTime);
        if (opened > 1) opened = 1;
        if (opened < 0) opened = 0;

        Debug.Log(transform.eulerAngles.y);

        //opened2 = (360 - transform.eulerAngles.z)/175;
        opened2 += vector2.axis.x * Time.deltaTime;
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
            myObject.xyz.Add(((gameObject.transform.position.z * -1) + start_pos.z) * multiplayer + coords_delay.x);
            myObject.xyz.Add((gameObject.transform.position.x - start_pos.x) * multiplayer + coords_delay.z);
            myObject.xyz.Add((gameObject.transform.position.y - start_pos.y) * multiplayer + coords_delay.y);
            myObject.speed = speed;
            myObject.opened = opened;
            myObject.rotation = transform.eulerAngles.y;
            myObject.rotation2 = opened2 * 360;
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
                    return_text[1] = return_text[1].Replace(".", sp);
                    float float1 = float.Parse(return_text[1]);
                    scr.alf1 = -float1 * Mathf.Rad2Deg;

                    return_text[1] = return_text[1].Replace(".", sp);
                    float1 = float.Parse(return_text[1]);
                    scr.table = -float1 * Mathf.Rad2Deg + 90;

                    return_text[3] = return_text[3].Replace(".", sp);
                    float1 = float.Parse(return_text[3]);
                    scr.alf2 = -float1 * Mathf.Rad2Deg;

                    return_text[4] = return_text[4].Replace(".", sp);
                    float1 = float.Parse(return_text[4]);
                    scr.alf3 = -float1 * Mathf.Rad2Deg;
                    scr.alf3 = opened2 * 180 - 90;
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
