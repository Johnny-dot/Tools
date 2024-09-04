package com.Fancy.Application;

import javax.microedition.khronos.egl.EGL10;
import javax.microedition.khronos.egl.EGLConfig;
import javax.microedition.khronos.egl.EGLDisplay;

import android.app.ActivityManager;
import android.content.Context;
import android.content.pm.ConfigurationInfo;
import android.content.res.AssetManager;
import android.content.res.Configuration;
import android.graphics.PixelFormat;
import android.opengl.GLSurfaceView;
import android.view.KeyEvent;
import android.view.MotionEvent;
import android.view.inputmethod.BaseInputConnection;
import android.view.inputmethod.EditorInfo;
import android.view.inputmethod.InputConnection;
import android.view.inputmethod.InputMethodManager;

public class FancyGLSurface extends GLSurfaceView
{
	protected FancyGLRenderer renderer;
	private float orgDis;
	private boolean MultilineTextfieldMode;

	private boolean detectOpenGLES30( )
	{
		ActivityManager am = (ActivityManager)UIGlobal.active.getSystemService(Context.ACTIVITY_SERVICE);  
		ConfigurationInfo info = am.getDeviceConfigurationInfo();  

		return info.reqGlEsVersion >= 0x30000;
	}

	public FancyGLSurface( Context context, String foaparam, String filename, AssetManager asset, String wPath )
	{
		super( context );

		int esversion = 2;
		// if ( detectOpenGLES30( ) )
			// esversion = 3;

		setEGLContextClientVersion(esversion);

		System.out.println( "ES Version" + esversion );

		try
		{
			setEGLConfigChooser( new ConfigChooser( 8, 8, 8, 8, 8 ) );
			getHolder( ).setFormat( PixelFormat.RGBA_8888 );
		}
		catch( Exception e )
		{
			System.out.println( "Unsupport EGL Config!!" );
		}

		renderer = new FancyGLRenderer( this, foaparam, filename, asset, wPath, esversion );
		setRenderer( renderer );
		setRenderMode( GLSurfaceView.RENDERMODE_WHEN_DIRTY );
		orgDis = 0;

		setFocusable( true );
		setFocusableInTouchMode( true );
	}

	float Distance( float x1, float y1, float x2, float y2 )
	{
		float x = x2 - x1;
		float y = y2 - y1;
		return (float) java.lang.Math.sqrt( x * x + y * y );
	}

	@Override
	public InputConnection onCreateInputConnection( EditorInfo outAttrs ) 
	{
		outAttrs.imeOptions = ( ( !MultilineTextfieldMode ? EditorInfo.IME_ACTION_DONE : 0 ) |
				EditorInfo.IME_FLAG_NO_EXTRACT_UI );
		return new GLViewInputConnection( this );
	}

	@Override
	public boolean onCheckIsTextEditor( )  
	{
		return true;
	}

	private class ConfigChooser implements GLSurfaceView.EGLConfigChooser
	{
		private int mRedSize;
		private int mGreenSize;
		private int mBuleSize;
		private int mAlphaSize;
		private int mStencilSize;

		public ConfigChooser( int redSize, int greenSize, int buleSize, int alphaSize, int stencilSize )
		{
			mRedSize = redSize;
			mGreenSize = greenSize;
			mBuleSize = buleSize;
			mAlphaSize = alphaSize;
			mStencilSize = stencilSize;
		}

		public EGLConfig chooseConfig( EGL10 egl, EGLDisplay display )
		{
			int[] searchattr = new int[]
			{
				EGL10.EGL_RED_SIZE, mRedSize,
				EGL10.EGL_GREEN_SIZE, mGreenSize,
				EGL10.EGL_BLUE_SIZE, mBuleSize,
				EGL10.EGL_ALPHA_SIZE, mAlphaSize,
				EGL10.EGL_STENCIL_SIZE, mStencilSize,
				EGL10.EGL_RENDERABLE_TYPE, 4,
				EGL10.EGL_NONE
			};
			int[] nconfigs = new int[1];
			egl.eglChooseConfig( display, searchattr, null, 0, nconfigs );
			EGLConfig[] configs = new EGLConfig[ nconfigs[0] ];
			egl.eglChooseConfig( display, searchattr, configs, nconfigs[0], nconfigs );

			int depthSize = 0;
			EGLConfig config = configs[0];
			for( EGLConfig config1 : configs )
			{
				int[] attr = new int[1];
				if ( egl.eglGetConfigAttrib( display, config1, EGL10.EGL_DEPTH_SIZE, attr ) && attr[0] > depthSize )
				{
					depthSize = attr[0];
					config = config1;
				}
			}

			return config;
		}
	}

	private static class GLViewInputConnection extends BaseInputConnection 
	{
		FancyGLSurface	mView;
		public GLViewInputConnection( FancyGLSurface view ) 
		{
			super( view, false );
			mView = view;
		}

		@Override
		public boolean sendKeyEvent( KeyEvent event ) 
		{
			int c = event.getKeyCode( );

			switch ( event.getAction( ) ) 
			{
				case KeyEvent.ACTION_DOWN:
				{
					if ( c == KeyEvent.KEYCODE_ENTER ) 
					{
						if ( ( event.getFlags( ) & KeyEvent.FLAG_EDITOR_ACTION ) != 0 && mView.getMultilineTextfieldMode( ) == false )
						{
							synchronized( FancyGLRenderer.render )
							{
								FancyMessage msg = new FancyMessage( );
								msg.mType = FancyMessage._EVENT_GFXEDIT_CHANGE;
								msg.mKey = UIMsgHandler.LOSEFOCUS;
								FancyGLRenderer.mMessages.add( msg );
							}

							InputMethodManager imm = (InputMethodManager) UIGlobal.active.getSystemService( Context.INPUT_METHOD_SERVICE );
							if ( imm != null )
							{
								if ( UIGlobal.active.getResources( ).getConfiguration( ).hardKeyboardHidden == Configuration.HARDKEYBOARDHIDDEN_YES )
									imm.hideSoftInputFromWindow( UIGlobal.glView.getWindowToken( ), InputMethodManager.HIDE_NOT_ALWAYS );
							}

							return true;
						}

						// Convert to GFx Key::Code::Return
						c = 13;
					}
					else if ( c == KeyEvent.KEYCODE_DEL )
					{
						// Convert to GFx Key::Code::Backspace
						c = 8;
					}
					else 
					{
						c = event.getUnicodeChar( event.getMetaState( ) );

						synchronized( FancyGLRenderer.render )
						{
							FancyMessage msg = new FancyMessage( );
							msg.mType = FancyMessage._EVENT_CHAR;
							msg.mKey = c;
							FancyGLRenderer.mMessages.add( msg );
						}

						return true;
					}

					synchronized( FancyGLRenderer.render )
					{
						FancyMessage msg = new FancyMessage( );
						msg.mType = FancyMessage._EVENT_KEYDOWN;
						msg.mKey = c;
						FancyGLRenderer.mMessages.add( msg );
					}

					return true;
				}

				case KeyEvent.ACTION_UP:
				{
					if ( c == KeyEvent.KEYCODE_ENTER ) 
					{
						// Convert to GFx Key::Code::Return
						c = 13;
					}
					else if ( c == KeyEvent.KEYCODE_DEL )
					{
						// Convert to GFx Key::Code::Backspace
						c = 8;
					}
					else 
					{
						// Ignore other codes
						return true;
					}

					synchronized( FancyGLRenderer.render )
					{
						FancyMessage msg = new FancyMessage( );
						msg.mType = FancyMessage._EVENT_KEYUP;
						msg.mKey = c;
						FancyGLRenderer.mMessages.add( msg );
					}

					return true;
				}

				case KeyEvent.ACTION_MULTIPLE:
				{
					if ( event.getKeyCode( ) == KeyEvent.KEYCODE_UNKNOWN ) 
					{
						String chars = event.getCharacters( );
						if ( chars != null ) 
						{
							for ( int i = 0; i < chars.length( ); i ++ ) 
							{
								c = chars.charAt( i );

								synchronized( FancyGLRenderer.render )
								{
									FancyMessage msg = new FancyMessage( );
									msg.mType = FancyMessage._EVENT_CHAR;
									msg.mKey = c;
									FancyGLRenderer.mMessages.add( msg );
								}
							}
						}
					}

					return true;
				}
			}

			return true;
		}
	}

	@Override
	public boolean onTouchEvent( MotionEvent event )
	{
		final int count = event.getPointerCount( );
		switch ( event.getAction( ) & event.getActionMasked( ) ) 
		{
			case MotionEvent.ACTION_DOWN:
			{
				final float x1 = event.getX( 0 );
				final float y1 = event.getY( 0 );
				if ( count == 2 )
				{
					float x2 = event.getX( 1 );
					float y2 = event.getY( 1 );
					orgDis = Distance( x1, y1, x2, y2 );
				}
				else if ( count == 1 )
				{
					this.queueEvent( new Runnable( )
					{
						@Override
						public void run( )
						{
							FancyGLRenderer.render.TouchBeginMessage( 0, (int) x1, (int) y1, count );
						}
					} );
				}
			}
			break;

			case MotionEvent.ACTION_MOVE:
			{
				final float x1 = event.getX(0);
				final float y1 = event.getY(0);

				if ( count == 2 )
				{
					float x2 = event.getX(1);
					float y2 = event.getY(1);
					
					float curDis = Distance( x1, y1, x2, y2 );

					if ( orgDis == 0 )
						orgDis = curDis;
					final float dis = curDis - orgDis;
					
					this.queueEvent( new Runnable( )
					{
						@Override  
						public void run( )
						{
							FancyGLRenderer.render.TouchZoomMessage( 0, dis, count );
						}
					} );
					
					orgDis = curDis;
				}
				else if ( count == 1 )
				{
					this.queueEvent( new Runnable( )
					{
						@Override
						public void run( )
						{
							FancyGLRenderer.render.TouchMoveMessage( 0, (int) x1, (int) y1, count );
						}
					} );
				}
			}
			break;

			case MotionEvent.ACTION_POINTER_UP:
			{
				if ( count == 2 )
				{
					final int x = (int) event.getX( event.getActionIndex( ) );
					final int y = (int) event.getY( event.getActionIndex( ) );
					this.queueEvent( new Runnable( )
					{
						@Override
						public void run( )
						{
							FancyGLRenderer.render.TouchEndMessage( 0, x, y, count );
						}
					} );
				}
			}
			break;

			case MotionEvent.ACTION_UP:
			{
				final int x = (int) event.getX(0);
				final int y = (int) event.getY(0);

				orgDis = 0;
				this.queueEvent( new Runnable( )
				{
					@Override
					public void run( )
					{
						FancyGLRenderer.render.TouchEndMessage( 0, x, y, count );
					}
				} );
			}
			break;
		}
		
		return true;
	}

	public void setMultilineTextfieldMode( boolean mode )
	{
		MultilineTextfieldMode = mode;
	}

	public boolean getMultilineTextfieldMode( )
	{
		return MultilineTextfieldMode;
	}

	public void destroy( )
	{
		renderer.destroy( );
	}
}