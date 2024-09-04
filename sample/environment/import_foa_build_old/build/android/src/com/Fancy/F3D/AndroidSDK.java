
package com.Fancy.F3D;

import com.Fancy.Application.UIGlobal;

import android.os.Looper;
import android.util.Log;

public class AndroidSDK
{
	private boolean looperinited = false;
	public int sdkcommand( String cmdstr )
	{
		if ( looperinited == false )
		{
			Looper.prepare();
			looperinited = true;
		}

		System.out.println( cmdstr );

		String[] cmds = cmdstr.split("::");
		int ret = 0;
		if ( cmds.length <= 1 )
			return ret;

		if ( cmds[0].equals("360") )
		{
			//ret = SDK360.command( cmds[1] );
		}
		else if ( cmds[0].equals("talkingdata") )
		{
			//ret = SDKtalkingdata.command( cmds[1] );
		}
		else if ( cmds[0].equals("mta") )
		{
			//ret = SDKmta.command( cmds[1] );
		}
		else if ( cmds[0].equals("upay") )
		{
			//ret = SDKupay.command( cmds[1] );
		}
		else if ( cmds[0].equals("iapppay") )
		{
			//ret = SDKiapppay.command( cmds[1] );
		}
		else if ( cmds[0].equals("anzhi") )
		{
			//ret = SDKanzhi.command( cmds[1] );
		}
		else if ( cmds[0].equals("xiaomi") )
		{
			//ret = SDKxiaomi.command( cmds[1] );
		}
		else if ( cmds[0].equals("statistics") )
		{
			ret = SDKstatistics.command( cmds[1] );
		}
		
		else if ( cmds[0].equals("weixin") )
		{
			//ret = SDKweixin.getInstance( ).command( cmds[1] );
		}

		return ret;
	}
}