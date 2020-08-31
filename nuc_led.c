/*
 * Low-level Intel NUC LED Control Driver
 *
 * Copyright (C) 2020 Johannes Ernst
 *
 * Portions based on nuc_led.c for NUC 6, 7:
 * Copyright (C) 2017 Miles Peterson
 *
 * Portions based on asus-wmi.c:
 * Copyright (C) 2010 Intel Corporation.
 * Copyright (C) 2010-2011 Corentin Chary <corentin.chary@gmail.com>
 *
 * Portions based on acpi_call.c:
 * Copyright (C) 2010: Michal Kottman
 *
 * Based on Intel Article ID 000023426
 * http://www.intel.com/content/www/us/en/support/boards-and-kits/intel-nuc-kits/000023426.html
 * and Intel Article "WMI Interface for Intel NUC Products"
 * https://www.intel.com/content/dam/support/us/en/documents/intel-nuc/WMI-Spec-Intel-NUC-NUC10ixFNx.pdf
 *
 *  This program is free software; you can redistribute it and/or modify
 *  it under the terms of the GNU General Public License as published by
 *  the Free Software Foundation; either version 2 of the License, or
 *  (at your option) any later version.
 *
 *  This program is distributed in the hope that it will be useful,
 *  but WITHOUT ANY WARRANTY; without even the implied warranty of
 *  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 *  GNU General Public License for more details.
 *
 *  You should have received a copy of the GNU General Public License
 *  along with this program; if not, write to the Free Software
 *  Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA
 */

#define pr_fmt(fmt) KBUILD_MODNAME ": " fmt

#include <linux/module.h>
#include <linux/kernel.h>
#include <linux/types.h>
#include <linux/proc_fs.h>
#include <linux/acpi.h>
#include <linux/vmalloc.h>
#include <linux/uaccess.h>

MODULE_AUTHOR("Johannes Ernst");
MODULE_DESCRIPTION("Intel NUC LED Control WMI Driver");
MODULE_LICENSE("GPL");
ACPI_MODULE_NAME("NUC_LED");

static unsigned int nuc_led_perms __read_mostly = S_IRUGO | S_IWUSR | S_IWGRP;
static unsigned int nuc_led_uid __read_mostly;
static unsigned int nuc_led_gid __read_mostly;

module_param(nuc_led_perms, uint, S_IRUGO | S_IWUSR | S_IWGRP);
module_param(nuc_led_uid, uint, 0);
module_param(nuc_led_gid, uint, 0);

MODULE_PARM_DESC(nuc_led_perms, "permissions on /proc/acpi/nuc_led");
MODULE_PARM_DESC(nuc_led_uid, "default owner of /proc/acpi/nuc_led");
MODULE_PARM_DESC(nuc_led_gid, "default owning group of /proc/acpi/nuc_led");

/* Intel NUC WMI GUID */
#define NUCLED_WMI_MGMT_GUID "8C5DA44C-CDC3-46b3-8619-4E26D34390B7"
MODULE_ALIAS("wmi:" NUCLED_WMI_MGMT_GUID);

extern struct proc_dir_entry *acpi_root_dir;

#define INPUT_BUFFER_SIZE 5
static unsigned char input_buffer[INPUT_BUFFER_SIZE];

#define OUTPUT_BUFFER_SIZE 4
static unsigned char output_buffer[OUTPUT_BUFFER_SIZE];

/*
 * Invoked by the kernel when the device is written.
 */
static ssize_t acpi_proc_write(struct file *filp, const char __user *buff,
                size_t len, loff_t *data)
{
    char * kernelBuff;
    unsigned int kernelBuffI;
    unsigned int inputBufferI;
    unsigned int currentByte;
    unsigned int currentNibble;
    unsigned char c;
    int inWhite; // boolean

    struct acpi_buffer acpiInput;
    struct acpi_buffer acpiOutput = { ACPI_ALLOCATE_BUFFER, NULL };
    acpi_status acpiStatus;
    union acpi_object * acpiObjectP;
    int i;

    // Move buffer from user space to kernel space -- cannot access used space
    kernelBuff = vmalloc(len);
    if (!kernelBuff) {
        return -ENOMEM;
    }

    if (copy_from_user(kernelBuff, buff, len)) {
        return -EFAULT;
    }

    // parse hex
    currentByte = 0;
    inWhite     = 1;

    for(    kernelBuffI = 0, inputBufferI = 0 ;
            kernelBuffI < len && inputBufferI < INPUT_BUFFER_SIZE ;
            ++kernelBuffI )
    {
        c = kernelBuff[kernelBuffI];

        if( c >= '0' && c <= '9' ) {
            if( inWhite ) {
                inWhite     = 0;
                currentByte = 0;
            }
            currentNibble = c - '0';
            currentByte = ( currentByte << 4 ) + currentNibble;

        } else if( c >= 'a' && c <= 'f' ) {
            if( inWhite ) {
                inWhite     = 0;
                currentByte = 0;
            }
            currentNibble = c - 'a' + 10;
            currentByte = ( currentByte << 4 ) + currentNibble;

        } else if( c >= 'A' && c <= 'F' ) {
            if( inWhite ) {
                inWhite     = 0;
                currentByte = 0;
            }
            currentNibble = c - 'A' + 10;
            currentByte = ( currentByte << 4 ) + currentNibble;

        } else if( c == ' ' || c == '\t' || c == '\n' ) {
            if( !inWhite ) {
                inWhite = 1;
                input_buffer[ inputBufferI++ ] = currentByte;
                currentByte = 0;
            }

        } else {
            pr_warn("NUC LED invalid character: %c\n", c );
            return -EIO;
        }
    }
    if( !inWhite && inputBufferI < INPUT_BUFFER_SIZE ) {
        input_buffer[ inputBufferI++ ] = currentByte;
    }
    if( inputBufferI != 5 ) {
        pr_warn("NUC LED received wrong number of bytes (5 needed): %d\n", inputBufferI );
        return -EIO;
    }

    vfree(kernelBuff);

    // prepare wmi call

    acpiInput.length = (acpi_size) inputBufferI-1;
    acpiInput.pointer = input_buffer+1;

    pr_info( "NUC LED wmi_evaluate_method method=%02x, data: %02x %02x %02x %02x\n",
            (unsigned char) input_buffer[0],
            ((unsigned char *) acpiInput.pointer)[0],
            ((unsigned char *) acpiInput.pointer)[1],
            ((unsigned char *) acpiInput.pointer)[2],
            ((unsigned char *) acpiInput.pointer)[3] );

    acpiStatus = wmi_evaluate_method(NUCLED_WMI_MGMT_GUID, 0, input_buffer[0],
                                 &acpiInput, &acpiOutput);

    if (ACPI_FAILURE(acpiStatus)) {
        ACPI_EXCEPTION((AE_INFO, acpiStatus, "wmi_evaluate_method"));
        return -EIO;
    }

    // unpack wmi output

    acpiObjectP = (union acpi_object *)acpiOutput.pointer;

    // pr_info( "NUC LED WMI response has length: %d\n", acpiObjectP->buffer.length );

    for(    i = 0;
            i < acpiObjectP->buffer.length && i < OUTPUT_BUFFER_SIZE;
            ++i )
    {
        output_buffer[i] = ((const char *)acpiObjectP->buffer.pointer)[i];
    }

    kfree( acpiOutput.pointer );

    return len;
}

/*
 * Invoked by the kernel when the device is read.
 */
static ssize_t acpi_proc_read(struct file *filp, char __user *buff,
                size_t count, loff_t *off)
{
    int len;
    char line[16];
    ssize_t ret;

    sprintf( line, "%02x %02x %02x %02x\n", output_buffer[0], output_buffer[1], output_buffer[2], output_buffer[3] );

    len = strlen(line);
    ret = simple_read_from_buffer(buff, count, off, line, len + 1);

    // Clear buffer
    memset(output_buffer, 0xff, OUTPUT_BUFFER_SIZE);

    return ret;
}

/*
 * Table of ACPI device operations
 */
static struct proc_ops proc_acpi_operations = {
        .proc_read     = acpi_proc_read,
        .proc_write    = acpi_proc_write,
};

/*
 * Kernel module initialization
 */
static int __init init_nuc_led(void)
{
    struct proc_dir_entry *acpi_entry;
    kuid_t uid;
    kgid_t gid;

    // Make sure LED control WMI GUID exists
    if (!wmi_has_guid(NUCLED_WMI_MGMT_GUID)) {
        pr_warn("Intel NUC LED WMI GUID not found\n");
        return -ENODEV;
    }

    // Verify the user parameters
    uid = make_kuid(&init_user_ns, nuc_led_uid);
    gid = make_kgid(&init_user_ns, nuc_led_gid);

    if (!uid_valid(uid) || !gid_valid(gid)) {
        pr_warn("Intel NUC LED control driver got an invalid UID or GID\n");
        return -EINVAL;
    }

    // Clear buffer
    memset(output_buffer, 0xff, OUTPUT_BUFFER_SIZE);

    // Create nuc_led ACPI proc entry
    acpi_entry = proc_create("nuc_led", nuc_led_perms, acpi_root_dir, &proc_acpi_operations);

    if (acpi_entry == NULL) {
        pr_warn("Intel NUC LED control driver could not create proc entry\n");
        return -ENOMEM;
    }

    proc_set_user(acpi_entry, uid, gid);

    pr_info("Intel NUC LED control driver loaded\n");

    return 0;
}

/*
 * Kernel module exit
 */
static void __exit unload_nuc_led(void)
{
    remove_proc_entry("nuc_led", acpi_root_dir);
    pr_info("Intel NUC LED control driver unloaded\n");
}

/*
 * Register module functions
 */
module_init(init_nuc_led);
module_exit(unload_nuc_led);
