package com.Fancy.F3D;

import java.io.BufferedReader;
import java.io.File;
import java.io.FileNotFoundException;
import java.io.FileReader;
import java.io.IOException;
import java.util.Hashtable;
import java.util.UUID;

import com.Fancy.Application.NotificationService;
import com.Fancy.Application.UIGlobal;
import com.tencent.android.tpush.XGIOperateCallback;
import com.tencent.android.tpush.XGPushConfig;
import com.tencent.android.tpush.XGPushManager;

import android.app.Activity;
import android.app.ActivityManager;
import android.content.Context;
import android.content.res.AssetManager;
import android.content.res.Configuration;
import android.graphics.Bitmap;
import android.graphics.BitmapFactory;
import android.graphics.Canvas;
import android.graphics.Color;
import android.graphics.Paint;
import android.graphics.Typeface;
import android.net.ConnectivityManager;
import android.net.NetworkInfo;
import android.net.wifi.WifiInfo;
import android.net.wifi.WifiManager;
import android.opengl.GLSurfaceView;
import android.os.Build;
import android.os.Debug;
import android.os.Environment;
import android.os.Handler;
import android.os.Message;
import android.os.PowerManager;
import android.os.StatFs;
import android.telephony.TelephonyManager;
import android.util.DisplayMetrics;
import android.view.inputmethod.InputMethodManager;
import android.content.Intent;
import android.net.Uri;

public class FancyJni
{
	private native int JniInit( Object window, String uipackage, String foaparam, String filename, Object assetManager );
	private native int JniRender( int elapse );
	private native int JniMessageTouchBegin( int window, int x, int y, int count );
	private native int JniMessageTouchMove( int window, int x, int y, int count );
	private native int JniMessageTouchEnd( int window, int x, int y, int count );
	private native int JniMessageTouchZoom( int window, float distance, int count );
	private native int JniMessageButton( int window );
	private native int JniMessageSpinPrevious( int window );
	private native int JniMessageSpinNext( int window );
	private native int JniMessageTextChange( int window, boolean isTextArea );
	private native int JniMessageCheckBox( int window, boolean isSelected );
	private native int JniMessageTileList( int window );
	private native int JniMessageGfxEdit( int window, int key );
	private native int JniMessageBackButton( int window );
	private native int JniMessageActive( int window, boolean isActive );
	private native int JniMessageShakePhone( int window );
	private native int JniMessageResize( int window, int width, int height );
	private native int JniMessageNotify( int window, int id );
	private native int JniMessageKeyboard( int window, String str );
	private native int JniMessageNetChange( int window );
	private native int JniMessageKeyDown( int window, int key );
	private native int JniMessageKeyUp( int window, int key );
	private native int JniMessageChar( int window, int key );
	private native int JniMessageVisible( int window, int distance, int x1, int y1, int x2, int y2 );
	private native int JniMessageRestore( int window );
	private native int JniResize( );
	private native int JniDelete( Object window );
	private native int JniSDKResult( String result );
	private native static int JniMessagePayResult( int result, int errorcode, String paytype, int count, String productid, String tradeid, int amount );
	private native static int JniRenderDevice( boolean devicelost );

	private static AssetManager		mAsset;
	private static String			mWritePath;
	private static int 				resolutionwidth;
	private static int				resolutionheight;
	private static float			resolutionwratio;
	private static float			resolutionhratio;
	private static int				esVersion;
	private static GLSurfaceView	glview;
	private PowerManager.WakeLock	mWakeLock;
	private static boolean			mInited = false;
	private static String 			mLastfont = "";
	private static int				mAppOrientation = 0;
	
	private static Handler mHandler = new Handler( )
	{
		@Override
		public void handleMessage( Message msg )
		{
			glview.getHolder( ).setFixedSize( resolutionwidth, resolutionheight );
		}
	};

	public FancyJni( GLSurfaceView view, AssetManager asset, String foaparam, int esversion )
	{
		glview				= view;
		mAsset				= asset;
		mWakeLock			= null;

		resolutionwidth = getPhysicalWidth( UIGlobal.active );
		resolutionheight = getPhysicalHeight( UIGlobal.active );
		resolutionwratio = 0.0f;
		resolutionhratio = 0.0f;
		esVersion = esversion;
		
		String[] params = foaparam.split( "\\|" );
		if ( params.length > 1 )
		{
			for ( int i = 0; i < params.length - 1; i += 2 )
			{
				if ( params[i].equals( "resolutionwidth" ) )
					resolutionwidth = Integer.parseInt( params[i + 1] );
				else if ( params[i].equals( "resolutionheight" ) )
					resolutionheight = Integer.parseInt( params[i + 1] );
				else if ( params[i].equals( "resolutionwratio" ) )
					resolutionwratio = Float.parseFloat( params[i + 1] );
				else if ( params[i].equals( "resolutionhratio" ) )
					resolutionhratio = Float.parseFloat( params[i + 1] );
			}
		}
	}

	public void FancyInit( Object window, String foa, String fn, String wPath )
	{
		mWritePath = wPath;
		
		if ( resolutionwratio > 0.0f )
			resolutionwidth = (int) ( getPhysicalWidth( window ) * resolutionwratio );

		if ( resolutionhratio > 0.0f )
			resolutionheight = (int) ( getPhysicalHeight( window ) * resolutionhratio );
		
		resolutionwidth = resolutionwidth > 0 ? resolutionwidth : getPhysicalWidth( window );
		resolutionheight = resolutionheight > 0 ? resolutionheight : getPhysicalHeight( window );
		
		mHandler.sendEmptyMessage( 0 );
		JniInit( window, "com/Fancy/F3D", foa, fn, mAsset );
		JniMessageResize( 0, resolutionwidth, resolutionheight );
		mInited = true;
	}

	public void FancyMessageTouchBegin( int window, int x, int y, int count )
	{
		JniMessageTouchBegin( window, x, y, count );
	}

	public void FancyMessageTouchMove( int window, int x, int y, int count )
	{
		JniMessageTouchMove( window, x, y, count );
	}

	public void FancyMessageTouchEnd( int window, int x, int y, int count )
	{
		JniMessageTouchEnd( window, x, y, count );
	}

	public void FancyMessageTouchZoom( int window, float distance, int count )
	{
		JniMessageTouchZoom( window, distance, count );
	}

	public void FancyMessageButton( int window )
	{
		JniMessageButton( window );
	}

	public void FancyMessageSpinPrevious( int window )
	{
		JniMessageSpinPrevious( window );
	}

	public void FancyMessageSpinNext( int window )
	{
		JniMessageSpinNext( window );
	}

	public void FancyMessageTextChange( int window, boolean isTextArea )
	{
		JniMessageTextChange( window, isTextArea );
	}

	public void FancyMessageCheckBox( int window, boolean isSelected )
	{
		JniMessageCheckBox( window, isSelected );
	}

	public void FancyMessageTileList( int window )
	{
		JniMessageTileList( window );
	}

	public void FancyMessageGfxEdit( int window, int key )
	{
		JniMessageGfxEdit( window, key );
	}

	public void FancyMessageBackButton( int window )
	{
		JniMessageBackButton( window );
	}

	public void FancyMessageActive( int window, boolean isActive )
	{
		JniMessageActive( window, isActive );
	}

	public void FancyMessageShakePhone( int window )
	{
		JniMessageShakePhone( window );
	}

	public void FancyMessageResize( int window )
	{
		JniMessageResize( window, resolutionwidth, resolutionheight );
	}

	public void FancyMessageNotify( int window, int id )
	{
		JniMessageNotify( window, id );
	}

	public void FancyMessageKeyboard( int window, String str )
	{
		JniMessageKeyboard( window, str );
	}

	public void FancyMessageNetChange( int window )
	{
		JniMessageNetChange( window );
	}

	public void FancyMessageKeyDown( int window, int key )
	{
		JniMessageKeyDown( window, key );
	}

	public void FancyMessageKeyUp( int window, int key )
	{
		JniMessageKeyUp( window, key );
	}

	public void FancyMessageChar( int window, int key )
	{
		JniMessageChar( window, key );
	}

	public void FancyMessageVisibleTextbox( int window, int height, int x1, int y1, int x2, int y2 )
	{
		JniMessageVisible( window, getDeviceHeight( ) - height, x1, y1, x2, y2 );
	}

	public void FancyMessageRestore( int window )
	{
		JniMessageRestore( window );
	}

	public void FancyRender( int e )
	{
		JniRender( e );
	}
	
	public void FancyResize( )
	{
		JniResize( );
	}
	
	public void Present( )
	{
		glview.requestRender( );
	}
	
	public void FancyDelete( Object window )
	{
		JniDelete( window );
	}

	public void FancyMessageSDKResult( String result )
	{
		JniSDKResult( result );
	}

	public static void FancyMessagePayResult( int result, int errorcode, String paytype, int count, String productid, String tradeid, int amount )
	{
		if ( mInited )
			JniMessagePayResult( result, errorcode, paytype, count, productid, tradeid, amount );
	}

	public static void FancyRenderDevice( boolean devicelost )
	{
		if ( mInited )
			JniRenderDevice( devicelost );
	}
	
	public static int getDeviceWidth( )
	{
		return resolutionwidth;
	}
	
	public static int getDeviceHeight( )
	{
		return resolutionheight;
	}

	public static void setAppOrientation( int orientation )
	{
		mAppOrientation = orientation;
	}

	public static int getPhysicalWidth( Object window )
	{
		Activity act = (Activity) window;
		if ( mAppOrientation == Configuration.ORIENTATION_LANDSCAPE && act.getWindowManager( ).getDefaultDisplay( ).getWidth( ) < act.getWindowManager( ).getDefaultDisplay( ).getHeight( ) )
			return act.getWindowManager( ).getDefaultDisplay( ).getHeight( );

		return act.getWindowManager( ).getDefaultDisplay( ).getWidth( );
	}
	
	public static int getPhysicalHeight( Object window )
	{
		Activity act = (Activity) window;
		if ( mAppOrientation == Configuration.ORIENTATION_LANDSCAPE && act.getWindowManager( ).getDefaultDisplay( ).getWidth( ) < act.getWindowManager( ).getDefaultDisplay( ).getHeight( ) )
			return act.getWindowManager( ).getDefaultDisplay( ).getWidth( );

		return act.getWindowManager( ).getDefaultDisplay( ).getHeight( );
	}

	public static int getESVersion( )
	{
		return esVersion;
	}

	public static Paint initFont( String name, int size, int glow, int edge, boolean bold, boolean italic, boolean underline, boolean strikeout, int space )
	{
		Paint p = new Paint( );
		p.setColor( Color.WHITE );
		p.setTextSize( size );
		p.setUnderlineText( underline );
		p.setFakeBoldText( bold );
		p.setAntiAlias( true );
		p.setStrikeThruText( strikeout );

		Typeface typeface;
		try
		{
			typeface = Typeface.createFromAsset( mAsset, "fonts/" + name + ".ttf" );
		}
		catch( Exception ex )
		{
			if ( ! mLastfont.equals( name ) )
			{
				System.out.println( "Lost font file: " + name + ".ttf" + ", used 'MONOSPACE' instead" );
				mLastfont = name;
			}
			typeface = Typeface.create( Typeface.MONOSPACE, bold ? Typeface.BOLD : Typeface.NORMAL );
		}

		p.setTypeface( typeface );

		if ( italic )
			p.setTextSkewX( -0.2f );

		return p;
	}

	public static int FontHeight( Paint p )
	{
		Paint.FontMetrics metrics = p.getFontMetrics( );
		return (int) ( metrics.bottom - metrics.top );
	}

	public static int [] FontBitmap( Paint p, String code, int fontspace, boolean italic, int size, int width, int height, int glow, int edge)
	{
		width = ( (int) p.measureText( code ) + 1 ) / 2 * 2;

		if ( italic )
			width = (int) ( width * 1.1 + 0.5 );

		Bitmap bitmap = Bitmap.createBitmap( width + fontspace, height, Bitmap.Config.ARGB_8888 );
		Canvas canvas = new Canvas( bitmap );
		canvas.drawColor( Color.BLACK );
		canvas.drawText( code, fontspace, (int) ( p.descent( ) - p.ascent( ) ), p );

		int [] pixels = new int[ bitmap.getWidth( ) * bitmap.getHeight( ) ];
		bitmap.getPixels( pixels, 0, bitmap.getWidth( ), 0, 0, bitmap.getWidth( ), bitmap.getHeight( ) );

		if ( bitmap != null && !bitmap.isRecycled( ) )
			bitmap.recycle( );

		return pixels;
	}

	public static int [] PassBack( Paint p, String code, boolean italic )
	{
		int [] retparas = new int[2];
		retparas[0] = ( (int) p.measureText( code ) + 1 ) / 2 * 2;

		retparas[1] = -1;

		if ( italic )
		{
			retparas[1] = (int) ( retparas[0] * 0.1 + 0.5 );
			retparas[0] += retparas[1];
		}

		return retparas;
	}

	public static String GetWritePath( )
	{
		return mWritePath;
	}

	public static String GetCPUIDString( )
	{
		try
		{
			BufferedReader buffer = new BufferedReader( new FileReader( "/proc/cpuinfo" ) );
			String text = null;
			String cpu = null;
			while ( ( text = buffer.readLine( ) ) != null )
			{
				String lower = text.toLowerCase( );
				if ( lower.contains( "hardware" ) )
				{
					String[] array = text.split( ":\\s+", 2 );
					cpu = array[1];
				}
			}

			buffer.close( );
			return cpu;
		}
		catch ( FileNotFoundException e )
		{
			e.printStackTrace( );
		}
		catch ( IOException e )
		{
			e.printStackTrace( );
		}

		return null;
	}

	public static void ReportOnStart( int step )
	{
		String mac = "";
		try{
			WifiManager wifi = (WifiManager) UIGlobal.active.getSystemService( Context.WIFI_SERVICE );
			WifiInfo info = wifi.getConnectionInfo( );
			mac = info.getMacAddress( );
		}catch( Exception e ){}

		SDKstatistics.command( "uid|" + mac + "|machine|" + Build.BRAND + Build.MODEL + "|op|game_init|dept|android|channel|default|step|" + step );
	}

	public static String GetMachine( )
	{
		return Build.BRAND + Build.MODEL;
	}

	public static int GetPPIX( )
	{
		DisplayMetrics dm = new DisplayMetrics( );
		UIGlobal.active.getWindowManager( ).getDefaultDisplay( ).getMetrics( dm );
		return (int) dm.xdpi;
	}
	
	public static int GetPPIY( )
	{
		DisplayMetrics dm = new DisplayMetrics( );
		UIGlobal.active.getWindowManager( ).getDefaultDisplay( ).getMetrics( dm );
		return (int) dm.ydpi;
	}

	public static int GetDensityDpi( )
	{
		DisplayMetrics dm = new DisplayMetrics( );
		UIGlobal.active.getWindowManager( ).getDefaultDisplay( ).getMetrics( dm );
		return dm.densityDpi;
	}

	public static long GetTotalMemory( )
	{
		StatFs stat = new StatFs( Environment.getDataDirectory( ).getPath( ) );
		return stat.getBlockSize( ) * stat.getBlockCount( );
	}

	public static long GetAvailableMemory( )
	{
		final ActivityManager activityManager = (ActivityManager) UIGlobal.active.getSystemService( Context.ACTIVITY_SERVICE );
		ActivityManager.MemoryInfo info = new ActivityManager.MemoryInfo( );
		activityManager.getMemoryInfo( info );
		return info.availMem;
	}

	public static int GetCurrentMemoryUsage( )
	{
		final ActivityManager activityManager = (ActivityManager) UIGlobal.active.getSystemService( Context.ACTIVITY_SERVICE );
		int[] pids = new int[] { android.os.Process.myPid() };
		Debug.MemoryInfo[] info = activityManager.getProcessMemoryInfo( pids );
		return info[0].getTotalPss( );
	}

    static public boolean IsExternalMemoryAvailable( )
    {
        return android.os.Environment.getExternalStorageState( ).equals( android.os.Environment.MEDIA_MOUNTED );
    }

    static public long GetAvailableInternalMemorySize( )
    {
        File path = Environment.getDataDirectory( );
        StatFs stat = new StatFs( path.getPath( ) );
        long blockSize = stat.getBlockSize( );
        long availableBlocks = stat.getAvailableBlocks( );
        return availableBlocks * blockSize;
    }

    static public long GetTotalInternalMemorySize( )
    {
        File path = Environment.getDataDirectory( );
        StatFs stat = new StatFs( path.getPath( ) );
        long blockSize = stat.getBlockSize( );
        long totalBlocks = stat.getBlockCount( );
        return totalBlocks * blockSize;
    }

    static public long GetAvailableExternalMemorySize( )
    {
        if ( ! IsExternalMemoryAvailable( ) )
			return 0;

         File path = Environment.getExternalStorageDirectory( );
         StatFs stat = new StatFs( path.getPath( ) );
         long blockSize = stat.getBlockSize( );
         long availableBlocks = stat.getAvailableBlocks( );
         return availableBlocks * blockSize;
    }

    static public long GetTotalExternalMemorySize( )
    {
        if ( ! IsExternalMemoryAvailable( ) )
			return 0;

        File path = Environment.getExternalStorageDirectory( );
        StatFs stat = new StatFs( path.getPath( ) );
        long blockSize = stat.getBlockSize( );
        long totalBlocks = stat.getBlockCount( );
        return totalBlocks * blockSize;
    }

	public static String getApplicationName( )
	{
        return UIGlobal.active.getPackageName( ); 
    }

	public static String GetOSVersion( )
	{
		return android.os.Build.VERSION.RELEASE;
	}

	public Bitmap getBitmap( byte[] buffer )
	{
		BitmapFactory.Options options = new BitmapFactory.Options( );
		options.inPurgeable = true;

		return BitmapFactory.decodeByteArray( buffer, 0, buffer.length, options );
	}

	public void releaseBitmap( Bitmap bitmap )
	{
		if ( bitmap != null && !bitmap.isRecycled( ) )
			bitmap.recycle( );
	}

	public void initKeyboard( )
	{
		UIGlobal.sendMessage( this, UIGlobal.LUA_UI_INIT_EDIT );
	}

	public void showKeyboard( String str )
	{
		UIGlobal.text = str;
		UIGlobal.sendMessage( this, UIGlobal.LUA_UI_SHOW_EDIT );
	}

	public void hideKeyboard( )
	{
		UIGlobal.sendMessage( this, UIGlobal.LUA_UI_HIDE_EDIT );
	}

	public void removeKeyboard( )
	{
		UIGlobal.sendMessage( this, UIGlobal.LUA_UI_REMOVE_EDIT );
	}

	public void browse( String url )
	{
		Intent intent = new Intent( );
		intent.setAction( "android.intent.action.VIEW" );
		Uri content_url = Uri.parse( url );
		intent.setData( content_url );
		intent.addFlags( Intent.FLAG_ACTIVITY_NEW_TASK );
		UIGlobal.active.startActivity( intent );
	}

	public void Exit( )
	{
		FancyDelete( UIGlobal.active );
		System.runFinalizersOnExit( true );
		System.exit( 0 );
	}

	public String macAddress( )
	{
		//Do well when wifi is down.
		WifiManager wifi = (WifiManager) UIGlobal.active.getSystemService( Context.WIFI_SERVICE );
		WifiInfo info = wifi.getConnectionInfo( );
		return info.getMacAddress( );
	}

	public String GetUUID( )
	{
		return UUID.randomUUID( ).toString( );
	}

	public void Prompt( String title, String context, int type )
	{
		Hashtable<String, String> ht = new Hashtable<String, String>( );
		ht.put( "title", title );
		ht.put( "context", context );
		ht.put( "type", String.valueOf( type ) );
		UIGlobal.sendMessage( ht, UIGlobal.PROMPT );
	}

	public void OnGettingFocus( boolean multiline, int x1, int y1, int x2, int y2 )
	{
		InputMethodManager imm = (InputMethodManager) UIGlobal.active.getSystemService( Context.INPUT_METHOD_SERVICE );
		if ( imm == null )
			return;

		UIGlobal.layout.getViewTreeObserver( ).removeGlobalOnLayoutListener( UIGlobal.globalLayoutListener );
		UIGlobal.layout.getViewTreeObserver( ).addOnGlobalLayoutListener( UIGlobal.globalLayoutListener );

		if ( UIGlobal.active.getResources( ).getConfiguration( ).hardKeyboardHidden == Configuration.HARDKEYBOARDHIDDEN_YES )
		{
			UIGlobal.glView.setMultilineTextfieldMode( multiline );

			if ( imm.isAcceptingText( ) == false )
				imm.restartInput( UIGlobal.glView );
			imm.showSoftInput( UIGlobal.glView, 0 );

			UIGlobal.x1 = x1;
			UIGlobal.y1 = y1;
			UIGlobal.x2 = x2;
			UIGlobal.y2 = y2;
		}
	}

	public void OnLoseFocus( )
	{
		InputMethodManager imm = (InputMethodManager) UIGlobal.active.getSystemService( Context.INPUT_METHOD_SERVICE );
		if ( imm == null )
			return;

		if ( UIGlobal.active.getResources( ).getConfiguration( ).hardKeyboardHidden == Configuration.HARDKEYBOARDHIDDEN_YES )
			imm.hideSoftInputFromWindow( UIGlobal.glView.getWindowToken( ), InputMethodManager.HIDE_NOT_ALWAYS );
	}

	public void wakeLock( boolean wake )
	{
		if ( wake )
		{
			if ( mWakeLock != null )
				mWakeLock.release( );
			PowerManager powerManager = (PowerManager) UIGlobal.active.getSystemService( Context.POWER_SERVICE );
			mWakeLock = powerManager.newWakeLock( PowerManager.SCREEN_BRIGHT_WAKE_LOCK, "FancyGuo" );
			mWakeLock.acquire( );
		}
		else
		{
			if ( mWakeLock != null )
			{
				mWakeLock.release( );
				mWakeLock = null;
			}
		}
	}

	public int GetNetworkState( )
	{
		ConnectivityManager connectivity = (ConnectivityManager) UIGlobal.active.getSystemService( Context.CONNECTIVITY_SERVICE );
		if ( connectivity == null )
			return 0;

		NetworkInfo info = connectivity.getActiveNetworkInfo( );
		if ( info == null )
			return 0;

		if ( info.getTypeName( ).equals( "WIFI" ) )
			return 1;
		else
		{
			switch ( info.getSubtype( ) )
			{
				case TelephonyManager.NETWORK_TYPE_GPRS:
				case TelephonyManager.NETWORK_TYPE_EDGE:
				case TelephonyManager.NETWORK_TYPE_CDMA:
				case TelephonyManager.NETWORK_TYPE_1xRTT:
				case TelephonyManager.NETWORK_TYPE_IDEN:
					return 2;
				case TelephonyManager.NETWORK_TYPE_UMTS:
				case TelephonyManager.NETWORK_TYPE_EVDO_0:
				case TelephonyManager.NETWORK_TYPE_EVDO_A:
				case TelephonyManager.NETWORK_TYPE_HSDPA:
				case TelephonyManager.NETWORK_TYPE_HSUPA:
				case TelephonyManager.NETWORK_TYPE_HSPA:
				case TelephonyManager.NETWORK_TYPE_EVDO_B:
				case TelephonyManager.NETWORK_TYPE_EHRPD:
				case TelephonyManager.NETWORK_TYPE_HSPAP:
					return 3;
				case TelephonyManager.NETWORK_TYPE_LTE:
					return 4;
			}

			String name = info.getSubtypeName( );
			name = name.toLowerCase( );
			if ( name.contains( "gprs" ) ||
				name.contains( "edge" ) ||
				name.contains( "cdma" ) ||
				name.contains( "1xrtt" ) ||
				name.contains( "iden" ) )
				return 2;
			else if ( name.contains( "umts" ) ||
					name.contains( "evdo" ) ||
					name.contains( "hsdpa" ) ||
					name.contains( "hsupa" ) ||
					name.contains( "ehrpd" ) ||
					name.contains( "hspap" ) )
				return 3;
			else if ( name.contains( "lte" ) )
				return 4;
		}

		return -1;
	}

	public void Notification( int id, String date, String title, String content )
	{
		Intent it = new Intent( UIGlobal.active, NotificationService.class );
		it.putExtra( "notifyid", id );
		it.putExtra( "notifydate", date );
		it.putExtra( "notifytitle", title );
		it.putExtra( "notifycontent", content );

		UIGlobal.active.startService( it );
	}

	public void RepeatNotification( int id, String date, String title, String content, int type )
	{
		Intent it = new Intent( UIGlobal.active, NotificationService.class );
		it.putExtra( "notifyid", id );
		it.putExtra( "notifydate", date );
		it.putExtra( "notifytitle", title );
		it.putExtra( "notifycontent", content );
		it.putExtra( "notifytype", type );

		UIGlobal.active.startService( it );
	}

	public void RemoteNotification( String account, String appid, String appkey )
	{
		Context context = UIGlobal.active.getApplicationContext( );
		XGPushConfig.setAccessId( context, Long.parseLong( appid ) );
		XGPushConfig.setAccessKey( context, appkey );
		XGPushManager.registerPush( context, "*" );
		XGPushManager.registerPush( context, account, new XGIOperateCallback( )
		{
			@Override
			public void onSuccess(Object data, int flag)
			{
				System.out.println( "[FG] Register remote notifiaction success." );
			}

			@Override
			public void onFail(Object data, int errCode, String msg)
			{
				System.out.println( "[FG] Register remote notifiaction fail, error msg is " + msg );
			}
		});
	}

	public void CancelNotification( int id )
	{
		Intent it = new Intent( UIGlobal.active, NotificationService.class );
		it.putExtra( "notifyid", id );
		it.putExtra( "cancel", true );
		UIGlobal.active.startService( it );
	}

	public void CancelAllNotification( )
	{
		Intent it = new Intent( UIGlobal.active, NotificationService.class );
		it.putExtra( "cancelall", true );
		UIGlobal.active.startService( it );
	}

	static
	{
		System.loadLibrary( "Fancy3D" );
	}
}