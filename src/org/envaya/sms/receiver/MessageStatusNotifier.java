/*
 * To change this template, choose Tools | Templates
 * and open the template in the editor.
 */
package org.envaya.sms.receiver;

import android.content.BroadcastReceiver;
import android.content.Context;
import android.content.Intent;
import android.net.Uri;
import android.os.Bundle;
import org.envaya.sms.App;

public class MessageStatusNotifier extends BroadcastReceiver {

    @Override
    public void onReceive(Context context, Intent intent) {
        App app = (App) context.getApplicationContext();
        Uri uri = intent.getData();
        
        Bundle extras = intent.getExtras();
        int index = extras.getInt(App.STATUS_EXTRA_INDEX);
        int numParts = extras.getInt(App.STATUS_EXTRA_NUM_PARTS);

        int resultCode = getResultCode();
        
        // uncomment to test retry on outgoing message failure
        /*              
        if (Math.random() > 0.4)
        {
            resultCode = SmsManager.RESULT_ERROR_NO_SERVICE;
        }        
        */
        
        app.notifyOutgoingMessageStatus(uri, resultCode, index, numParts);        
    }
}