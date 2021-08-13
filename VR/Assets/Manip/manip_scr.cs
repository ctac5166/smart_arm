using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class manip_scr : MonoBehaviour
{
    [Range(-275, 275)]
    public float table;
    public Transform table_bone;
    [Space(25)]
    [Range(-275, 275)]
    public float alf1;
    public Transform alf1_bone;
    [Space(25)]
    [Range(-275, 275)]
    public float alf2;
    public Transform alf2_bone;
    [Space(25)]
    [Range(-275, 275)]
    public float alf3;
    public Transform alf3_bone;
    [Space(25)]
    [Range(-275, 275)]
    public float alf4;
    public Transform alf4_bone;
    //[Space(25)]
    //[Range(-275, 275)]
    //public float grab1;
    public Transform grab1_bone;
    //[Space(25)]
    //[Range(-275, 275)]
    //public float grab2;
    public Transform grab2_bone;

    [Space(25)]
    [Range(-275, 275)]
    public float grab_open;


    private void Update()
    {
        table_bone.transform.eulerAngles = new Vector3(
            0,
            table, 0);
        alf1_bone.transform.eulerAngles = new Vector3(
            alf1,
            table, 0);
        alf2_bone.transform.eulerAngles = new Vector3(
            alf2 + alf1,
            table, 0);
        alf3_bone.transform.eulerAngles = new Vector3(
            alf3 + alf2 + alf1,
            table, 0);
        alf4_bone.transform.localEulerAngles = new Vector3(
            0,
            alf4, 0);
        grab1_bone.transform.localEulerAngles = new Vector3(
            grab_open, 0, 0
            );
        grab2_bone.transform.localEulerAngles = new Vector3(
            -grab_open, 0,0
            );
    }
}
