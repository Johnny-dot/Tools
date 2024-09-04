package com.Fancy.Application;

import org.fmod.FMODAudioDevice;

import com.Fancy.Application.ShakeListener.OnShakeListener;
import com.Fancy.F3D.FancyJni;
import com.tencent.android.tpush.XGPushManager;

import java.io.BufferedReader;
import java.io.FileNotFoundException;
import java.io.IOException;
import java.io.InputStream;
import java.io.InputStreamReader;
import java.util.ArrayList;
import java.util.List;

import android.net.ConnectivityManager;
import android.net.NetworkInfo;
import android.os.Bundle;
import android.os.CountDownTimer;
import android.app.Activity;
import android.content.BroadcastReceiver;
import android.content.Context;
import android.content.Intent;
import android.content.IntentFilter;
import android.content.pm.ApplicationInfo;
import android.content.pm.PackageManager;
import android.content.res.AssetManager;
import android.content.res.Configuration;
import android.graphics.BitmapFactory;

import android.view.Display;
import android.view.KeyEvent;
import android.view.MotionEvent;
import android.view.SurfaceHolder;
import android.view.View;
import android.view.View.OnTouchListener;
import android.view.ViewTreeObserver.OnGlobalLayoutListener;
import android.view.Window;
import android.view.WindowManager;
import android.view.SurfaceHolder.Callback;
import android.widget.AbsoluteLayout;
import android.widget.ImageView;

public class MainActivity extends Activity 
{
	private FancyGLSurface		mGLView;
	private List<String>		data = new ArrayList<String>( );
	private ShakeListener		mShakeListener = null;
	private BroadcastReceiver	mReceiver = null;
	private String				mLastType = "";
	private boolean				mOnce = false;
	public VideoView			mVideoView;
	private FMODAudioDevice mFMODAudioDevice = new FMODAudioDevice( );
	private SurfaceHolder mSurfaceHolder;

	@Override
	protected void onNewIntent(Intent intent) 
	{
		super.onNewIntent(intent);

		if ( intent != null )
		{
			int notifyid = intent.getIntExtra( "notifyid", -1 ); 
			if ( notifyid != -1 )
			{
				synchronized( FancyGLRenderer.render )
				{
					FancyMessage msg = new FancyMessage( );
					msg.mType = FancyMessage._EVENT_NOTIFY;
					msg.mKey = notifyid;
					FancyGLRenderer.mMessages.add( msg );
				}
			}
		}
	}

	@Override
	public void onStart( )
	{
		super.onStart( );
		mFMODAudioDevice.start( );
	}

	@Override
	protected void onPause( )
	{
		mVideoView.pause( );
		FancyJni.FancyRenderDevice( true );

		synchronized( FancyGLRenderer.render )
		{
			FancyMessage msg = new FancyMessage( );
			msg.mType = FancyMessage._EVENT_ACTIVE_STATE;
			msg.mIsSelect = false;
			FancyGLRenderer.mMessages.add( msg );
		}

		if ( mShakeListener != null )
			mShakeListener.stop( );

		super.onPause( );
	}

	@Override
	protected void onResume( )
	{
		mVideoView.resume( );
		if ( mOnce )
			mOnce = false;
		else
			FancyJni.FancyRenderDevice( false );

		// Must call requestRender when render mode is RENDERMODE_WHEN_DIRTY.
		if ( mGLView != null )
			mGLView.requestRender( );

		synchronized( FancyGLRenderer.render )
		{
			FancyMessage msg = new FancyMessage( );
			msg.mType = FancyMessage._EVENT_ACTIVE_STATE;
			msg.mIsSelect = true;
			FancyGLRenderer.mMessages.add( msg );
		}

		if ( mShakeListener != null )
			mShakeListener.start( );

		super.onResume( );
	}

	@Override
	public void onStop( )
	{
		mFMODAudioDevice.stop( );

		if ( mShakeListener != null )
			mShakeListener.stop( );

		super.onStop( );
	}

	@Override
	public void onDestroy( )
	{
		if ( mGLView != null )
			mGLView.destroy( );
		unregisterReceiver( mReceiver );

		super.onDestroy( );
	}

	@Override
	public boolean onKeyDown( int keyCode, KeyEvent event )
	{
		if ( keyCode == KeyEvent.KEYCODE_BACK )
		{
			synchronized( FancyGLRenderer.render ) 
			{
				FancyMessage msg = new FancyMessage( );
				msg.mType = FancyMessage._EVENT_BACK_BUTTON;
				FancyGLRenderer.mMessages.add( msg );
			}
		}

		return false;
	}

	protected void showLogo( )
	{
		System.out.println( "Show logo" );
		try {
			setContentView( R.layout.logo );
		    ImageView image = (ImageView) findViewById( R.id.imageBitmap );
		    AssetManager assets = getAssets();
		    InputStream assetFile = assets.open( "logo.png" );
			// Display it
		    image.setImageBitmap( BitmapFactory.decodeStream(assetFile) );

		    new CountDownTimer(2000,100) {
		    	@Override
		    	public void onTick(long millisUntilFinished) {}
		    	@Override
		    	public void onFinish() {
		    		setContentView( UIGlobal.glLayout );
		    	}
		    }.start();
		} catch (Exception e){
			e.printStackTrace( );
		}
	}

	@Override
	protected void onCreate( Bundle savedInstanceState ) 
	{
		super.onCreate( savedInstanceState );
		FancyJni.setAppOrientation( getResources( ).getConfiguration( ).orientation );
		mOnce = true;
		getWindow( ).setFlags( WindowManager.LayoutParams.FLAG_KEEP_SCREEN_ON, WindowManager.LayoutParams.FLAG_KEEP_SCREEN_ON );

		UIGlobal.active = this;
		UIGlobal.handler = new UIMsgHandler( );
		mVideoView = new VideoView( this );
		mVideoView.setVisibility( View.GONE );

		FancyJni.ReportOnStart( 0 );

		String text = "";
		try 
		{
			InputStream is = getAssets( ).open( "fancy-dev.cfg" );
			int size = is.available( );

			byte[] buffer = new byte[size];
			is.read( buffer );
			is.close( );

			text = new String( buffer, "GB2312" );
		}
		catch ( IOException e )
		{
			System.out.println( "[FG] Can not find fancy-dev.cfg" );
			return;
		}

		if ( text != "" )
		{
			requestWindowFeature( Window.FEATURE_NO_TITLE );
			XGPushManager.registerPush( UIGlobal.active.getApplicationContext( ) );

			mGLView = new FancyGLSurface( this, text, "", getAssets( ), getFilesDir( ).toString( ) );
			UIGlobal.glView = mGLView;
			UIGlobal.glLayout =  new AbsoluteLayout( this );
			setContentView( UIGlobal.glLayout );
			UIGlobal.CreateLayout( this );

			mSurfaceHolder = mVideoView.getHolder();

			final Display display = getWindowManager( ).getDefaultDisplay( );
			mSurfaceHolder.setFixedSize(display.getWidth( ), display.getWidth( ));  
	
			mSurfaceHolder.setType(SurfaceHolder.SURFACE_TYPE_PUSH_BUFFERS);
			UIGlobal.glLayout.addView( mGLView );
			UIGlobal.glLayout.addView(mVideoView);
			UIGlobal.glLayout.setOnTouchListener( new OnTouchListener( )
			{
				@Override
				public boolean onTouch( View v, MotionEvent event )
				{
					mVideoView.onTouchEvent( event );
					return true;
				}
			});
			UIGlobal.videoview = mVideoView;

			// TODO.
			UIGlobal.glLayout.getViewTreeObserver().addOnGlobalLayoutListener(new OnGlobalLayoutListener() {
				 @Override
		         public void onGlobalLayout( ) 
				 {
					 // display.getWidth( ), display.getWidth( )
					 // For reset viewport.
				 }
			});

			IntentFilter intenFilter = new IntentFilter( ConnectivityManager.CONNECTIVITY_ACTION );
			mReceiver = new BroadcastReceiver( )
			{
				@Override
				public void onReceive( Context context, Intent intent )
				{
					ConnectivityManager connectivity = (ConnectivityManager) UIGlobal.active.getSystemService( Context.CONNECTIVITY_SERVICE );
					if ( connectivity == null )
						return;

					NetworkInfo info = connectivity.getActiveNetworkInfo( );
					if ( info != null )
					{
						if ( mLastType.equals( info.getTypeName( ) ) )
							return;

						mLastType = info.getTypeName( );
					}

					synchronized( FancyGLRenderer.render ) 
					{
						FancyMessage msg = new FancyMessage( );
						msg.mType = FancyMessage._EVENT_NETCHANGE;
						FancyGLRenderer.mMessages.add( msg );
					}
				}
			};
			registerReceiver( mReceiver, intenFilter );

			mShakeListener = new ShakeListener( this );
			mShakeListener.setOnShakeListener( new OnShakeListener( )
			{
				@Override
				public void onShake( )
				{
					synchronized( FancyGLRenderer.render ) 
					{
						FancyMessage msg = new FancyMessage( );
						msg.mType = FancyMessage._EVENT_SHAKE;
						FancyGLRenderer.mMessages.add( msg );
					}
				}
			});
		}

		//showLogo( );
	}
	
	public String getApplicationName( )
	{ 
		PackageManager packageManager = null;
		ApplicationInfo applicationInfo = null;
		try
		{
			packageManager = getPackageManager( );
			applicationInfo = packageManager.getApplicationInfo( getPackageName( ), 0 );
		}
		catch ( PackageManager.NameNotFoundException e )
		{ applicationInfo = null; }

		String applicationName = (String) packageManager.getApplicationLabel( applicationInfo );
		return applicationName;
	}

	// TODO, Lock orientation.
	@Override 
	public void onConfigurationChanged( Configuration newConfig ) 
	{
		super.onConfigurationChanged( newConfig ); 

		mVideoView.getLayoutParams( ).width = FancyJni.getDeviceWidth( );
		mVideoView.getLayoutParams( ).height = FancyJni.getDeviceHeight( );
		mGLView.getLayoutParams( ).width = FancyJni.getDeviceWidth( );
		mGLView.getLayoutParams( ).height = FancyJni.getDeviceHeight( );
	}
	
	private List<String> getData( )
	{
		String[] files = null;
		try
		{
			files = getAssets( ).list( "Sample" );
		}
		catch ( IOException e )
		{
			// TODO Auto-generated catch block
			e.printStackTrace( );
		}

		for ( int i = 0; i < files.length; i ++ )
		{
			String name = files[i].toString( );
			String [] tmp = name.split( "/" );
			name = tmp[ tmp.length - 1 ];
			if ( name.substring( name.length( ) - "lua".length( ) ).equals( "lua" ) )
				data.add( name );
			}
		
		return data;
	}
	
	private String getPath( )
	{
		String sdcard = getSdCardPath( );
		String [] sdpath = sdcard.split( ";" );
		String path = null;

		if ( sdpath.length == 1 )
		{
			path = sdpath[0];
		}
		else
		{
			String [] tmp = sdpath[0].split( "/" );
			if ( tmp[ tmp.length - 1 ].equals( "sdcard2" ) || tmp[ tmp.length - 1 ].equals( "sdcard0" ) )
				path = sdpath[1];
			else
				path = sdpath[0];
		}
		
		return path;
	}
	
	private String getSdCardPath( )
	{
		String mount = new String( );

		try
		{
			Runtime runtime = Runtime.getRuntime( );
			Process proc = runtime.exec( "mount" );
			InputStream is = proc.getInputStream( );
			InputStreamReader isr = new InputStreamReader( is );
			String line;
			BufferedReader br = new BufferedReader( isr );
			
			while ( ( line = br.readLine( ) ) != null ) 
			{
				if ( line.contains( "secure" ) ) 
					continue;
				if ( line.contains( "asec" ) ) 
					continue;
				
				if ( line.contains( "fat" ) ) 
				{
					String columns[] = line.split( " " );
					if ( columns != null && columns.length > 1 )
						mount = mount.concat( columns[1] + ";" );
				}
				else if ( line.contains( "fuse" ) )
				{
					String columns[] = line.split( " " );
					if ( columns != null && columns.length > 1 ) 
						mount = mount.concat( columns[1] + ";" );
				}
			}

		}
		catch ( FileNotFoundException e )
		{ e.printStackTrace( ); }
		catch ( IOException e )
		{ e.printStackTrace( ); }
		
		return mount;
	}

	static
	{
		System.loadLibrary( "fmodex" );
	}
}
