package com.Fancy.Application;

import java.util.ArrayList;
import com.Fancy.F3D.FancyJni;
import javax.microedition.khronos.egl.EGLConfig;
import javax.microedition.khronos.opengles.GL10;

import android.content.res.AssetManager;
import android.opengl.GLSurfaceView;

public class FancyGLRenderer implements GLSurfaceView.Renderer
{
	private static AssetManager	mAsset;
	private static String		mFoaparam;

	private long			lastTime;
	private String			mfilename;
	private String			writePath;
	private FancyJni		jni;
	private GLSurfaceView	surfaceView;

	public static FancyGLRenderer			render;
	public static ArrayList<FancyMessage>	mMessages;

	public FancyGLRenderer( Object glsurface, String foaparam, String filename, AssetManager asset, String wPath, int esversion )
	{
		mfilename	= filename;
		mAsset		= asset;
		mFoaparam	= foaparam;
		writePath	= wPath;
		render		= this;
		surfaceView	= (GLSurfaceView) glsurface;
		mMessages	= new ArrayList<FancyMessage>( );
		lastTime	= 0;

		jni = new FancyJni( surfaceView, mAsset, foaparam, esversion );
	}
	
	@Override
	public void onSurfaceCreated( GL10 unused, EGLConfig config )
	{
		if ( mFoaparam == "" )
			mfilename = "Sample/" + mfilename;

		jni.FancyInit( UIGlobal.active, mFoaparam, mfilename, writePath );

		int notifyid = UIGlobal.active.getIntent( ).getIntExtra( "notifyid", -1 ); 
		if ( notifyid != -1 )
		{
			synchronized( render )
			{
				FancyMessage msg = new FancyMessage( );
				msg.mType = FancyMessage._EVENT_NOTIFY;
				msg.mKey = notifyid;
				mMessages.add( msg );
			}
		}

		FancyJni.ReportOnStart( 1 );
	}

	@Override
	public void onDrawFrame( GL10 unused )
	{
		long curTime = System.currentTimeMillis( );
		if ( lastTime == 0 )
			lastTime = curTime;
		jni.FancyRender( (int) ( curTime - lastTime ) );
		lastTime = curTime;

		if ( mMessages.isEmpty( ) != true && mMessages.get( 0 ) != null )
		{
			switch( mMessages.get( 0 ).mType )
			{
			case FancyMessage._EVENT_BUTTON_CLICK:
				synchronized( this )
				{
					jni.FancyMessageButton( mMessages.get( 0 ).mWindow );
				}
				break;
	
			case FancyMessage._EVENT_SPIN_PCLICK:
				synchronized( this )
				{
					jni.FancyMessageSpinPrevious( mMessages.get( 0 ).mWindow );
				}
				break;
				
			case FancyMessage._EVENT_SPIN_NCLICK:
				synchronized( this )
				{
					jni.FancyMessageSpinNext( mMessages.get( 0 ).mWindow );
				}
				break;
	
			case FancyMessage._EVENT_EDIT_CHANGE:
				synchronized( this )
				{
					jni.FancyMessageTextChange( mMessages.get( 0 ).mWindow, mMessages.get( 0 ).mIsArea );
				}
				break;
				
			case FancyMessage._EVENT_CHECK_SELECT:
				synchronized( this )
				{
					jni.FancyMessageCheckBox( mMessages.get( 0 ).mWindow, mMessages.get( 0 ).mIsSelect );
				}
				break;
				
			case FancyMessage._EVENT_TILELIST_CLICK:
				synchronized( this )
				{
					jni.FancyMessageTileList( mMessages.get( 0 ).mWindow );
				}
				break;
	
			case FancyMessage._EVENT_GFXEDIT_CHANGE:
				synchronized( this )
				{
					jni.FancyMessageGfxEdit( mMessages.get( 0 ).mWindow, mMessages.get( 0 ).mKey );
				}
				break;

			case FancyMessage._EVENT_BACK_BUTTON:
				synchronized( this )
				{
					jni.FancyMessageBackButton( mMessages.get( 0 ).mWindow );
				}
				break;

			case FancyMessage._EVENT_ACTIVE_STATE:
				synchronized( this )
				{
					jni.FancyMessageActive( mMessages.get( 0 ).mWindow, mMessages.get( 0 ).mIsSelect );
				}
				break;

			case FancyMessage._EVENT_SHAKE:
				synchronized( this )
				{
					jni.FancyMessageShakePhone( mMessages.get( 0 ).mWindow );
				}
				break;

			case FancyMessage._EVENT_NOTIFY:
				synchronized( this )
				{
					jni.FancyMessageNotify( mMessages.get( 0 ).mWindow, mMessages.get( 0 ).mKey );
				}
				break;

			case FancyMessage._EVENT_KEYBOARD:
				synchronized( this )
				{
					jni.FancyMessageKeyboard( mMessages.get( 0 ).mWindow, mMessages.get( 0 ).mStr );
				}
				break;

			case FancyMessage._EVENT_NETCHANGE:
				synchronized( this )
				{
					jni.FancyMessageNetChange( mMessages.get( 0 ).mWindow );
				}
				break;

			case FancyMessage._EVENT_KEYDOWN:
				synchronized( this )
				{
					jni.FancyMessageKeyDown( mMessages.get( 0 ).mWindow, mMessages.get( 0 ).mKey );
				}
				break;


			case FancyMessage._EVENT_KEYUP:
				synchronized( this )
				{
					jni.FancyMessageKeyUp( mMessages.get( 0 ).mWindow, mMessages.get( 0 ).mKey );
				}
				break;

			case FancyMessage._EVENT_CHAR:
				synchronized( this )
				{
					jni.FancyMessageChar( mMessages.get( 0 ).mWindow, mMessages.get( 0 ).mKey );
				}
				break;

			case FancyMessage._EVENT_VISIBLE_TEXTBOX:
				synchronized( this )
				{
					jni.FancyMessageVisibleTextbox( mMessages.get( 0 ).mWindow, mMessages.get( 0 ).mKeyboardHeight, mMessages.get( 0 ).mX1, mMessages.get( 0 ).mY1, mMessages.get( 0 ).mX2, mMessages.get( 0 ).mY2 );
				}
				break;

			case FancyMessage._EVENT_RESTORE_TEXTBOX:
				synchronized( this )
				{
					jni.FancyMessageRestore( mMessages.get( 0 ).mWindow );
				}
				break;

			case FancyMessage._EVENT_SDK_RESULT:
				synchronized( this )
				{
					jni.FancyMessageSDKResult( mMessages.get( 0 ).mStr );
				}
				break;
			}
			mMessages.remove( 0 );
		}
	}
	
	public void TouchBeginMessage( int window, int x, int y, int count )
	{
		x = x * FancyJni.getDeviceWidth( ) / FancyJni.getPhysicalWidth( UIGlobal.active );
		y = y * FancyJni.getDeviceHeight( ) / FancyJni.getPhysicalHeight( UIGlobal.active );
		jni.FancyMessageTouchBegin( window, x, y, count );
	}

	public void TouchMoveMessage( int window, int x, int y, int count )
	{
		x = x * FancyJni.getDeviceWidth( ) / FancyJni.getPhysicalWidth( UIGlobal.active );
		y = y * FancyJni.getDeviceHeight( ) / FancyJni.getPhysicalHeight( UIGlobal.active );
		jni.FancyMessageTouchMove( window, x, y, count );
	}

	public void TouchEndMessage( int window, int x, int y, int count )
	{
		x = x * FancyJni.getDeviceWidth( ) / FancyJni.getPhysicalWidth( UIGlobal.active );
		y = y * FancyJni.getDeviceHeight( ) / FancyJni.getPhysicalHeight( UIGlobal.active );
		jni.FancyMessageTouchEnd( window, x, y, count );
	}

	public void TouchZoomMessage( int window, float distance, int count )
	{
		jni.FancyMessageTouchZoom( window, distance, count );
	}

	@Override
	public void onSurfaceChanged( GL10 unused, int width, int height )
	{
		jni.FancyResize( );
	}

	public void destroy( )
	{
		jni.Exit( );
	}
}