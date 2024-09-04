package com.Fancy.F3D;

import org.apache.http.client.methods.HttpGet;
import org.apache.http.impl.client.DefaultHttpClient;
import android.net.Uri;

public class SDKstatistics
{
	private static String mUrl = "http://datarep.fancy3d.com:8010/monitor?";

	public static int command( final String string )
	{
		new Thread( new Runnable( )
		{
			@Override
			public void run( )
			{
				String url = mUrl;
				String[] params = string.split( "\\|" );
				try
				{
					for ( int i = 0; i < params.length; i ++ )
					{
						if ( i % 2 == 0 )
							url += Uri.encode(params[i], "UTF-8") + "=";
						else if ( i == params.length - 1 )
							url += Uri.encode(params[i], "UTF-8");
						else
							url += Uri.encode(params[i], "UTF-8") + "&";
					}

					System.out.println( "url :" + url );

					HttpGet hg = new HttpGet( url );
					new DefaultHttpClient( ).execute( hg );
				}
				catch ( Exception e )
				{
					e.printStackTrace( );
				}
			}
		} ).start( );

		return 0;
	}

}
