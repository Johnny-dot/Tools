package com.Fancy.Application;

import java.util.Hashtable;

import com.Fancy.F3D.AndroidVideo;
import com.Fancy.F3D.AndroidButton;
import com.Fancy.F3D.AndroidCheckBox;
import com.Fancy.F3D.AndroidPanel;
import com.Fancy.F3D.AndroidSpin;
import com.Fancy.F3D.AndroidTextArea;
import com.Fancy.F3D.AndroidTextInput;
import com.Fancy.F3D.AndroidLabel;
import com.Fancy.F3D.AndroidTileList;
import com.Fancy.F3D.AndroidUI;
import com.Fancy.F3D.FancyJni;

import android.annotation.SuppressLint;
import android.app.AlertDialog;
import android.content.Context;
import android.content.DialogInterface;
import android.graphics.Color;
import android.graphics.Rect;
import android.graphics.drawable.StateListDrawable;

import android.os.Handler;
import android.os.Looper;
import android.os.Message;
import android.text.Editable;
import android.text.InputType;
import android.text.TextUtils;
import android.text.TextWatcher;
import android.util.TypedValue;

import android.view.Gravity;
import android.view.KeyEvent;

import android.view.View;
import android.view.ViewGroup;
import android.view.ViewTreeObserver;

import android.view.View.OnClickListener;
import android.view.inputmethod.EditorInfo;
import android.view.inputmethod.InputMethodManager;
import android.widget.AbsoluteLayout;
import android.widget.AdapterView;
import android.widget.AdapterView.OnItemClickListener;
import android.widget.ArrayAdapter;
import android.widget.Button;
import android.widget.EditText;
import android.widget.ImageView;
import android.widget.ImageView.ScaleType;
import android.widget.ListView;
import android.widget.RelativeLayout;
import android.widget.TextView;
import android.widget.TextView.OnEditorActionListener;


public class UIMsgHandler extends Handler
{
	public static final int BACKSPACE = 8;
	public static final int LOSEFOCUS = 10;

	public UIMsgHandler( )
	{
	}
	
	public UIMsgHandler( Looper looper )
	{
		super( looper );
	}

	@SuppressLint("NewApi")
	public void handleMessage( Message msg )
	{
		switch ( msg.what ) 
		{
			case UIGlobal.SET_X:
			{
				AndroidUI ui = (AndroidUI) msg.obj;
				( (AbsoluteLayout.LayoutParams) ui.mUI.getLayoutParams( ) ).x = ui.mX;
			}
			break;
	
			case UIGlobal.SET_Y:
			{
				AndroidUI ui = (AndroidUI) msg.obj;
				( (AbsoluteLayout.LayoutParams) ui.mUI.getLayoutParams( ) ).y = ui.mY;
			}
			break;

			case UIGlobal.SET_W:
			{
				AndroidUI ui = (AndroidUI) msg.obj;
				ui.mUI.getLayoutParams( ).width = ui.mW;
			}
			break;

			case UIGlobal.SET_H:
			{
				AndroidUI ui = (AndroidUI) msg.obj;
				ui.mUI.getLayoutParams( ).height = ui.mH;
			}
			break;

			case UIGlobal.SET_ENABLE:
			{
				AndroidUI ui = (AndroidUI) msg.obj;
				ui.mUI.setEnabled( ui.mIsEnable );
			}
			break;

			case UIGlobal.SET_SHOW:
			{
				AndroidUI ui = (AndroidUI) msg.obj;
				if ( ui.mIsShow )
					ui.mUI.setVisibility( View.VISIBLE );
				else
					ui.mUI.setVisibility( View.GONE );
			}
			break;

			case UIGlobal.SET_TOP:
			{
				AndroidUI ui = (AndroidUI) msg.obj;
				ui.mUI.bringToFront( );
				ui.mUI.requestLayout( );
				ui.mUI.invalidate( );
			}
			break;

			case UIGlobal.BUTTON:
			{
				final AndroidUI button = (AndroidUI) msg.obj;
				button.mUI = new Button( UIGlobal.active );
				button.mUI.setVisibility( View.GONE );
				( (Button) button.mUI ).setSingleLine( );
				( (Button) button.mUI ).setGravity( Gravity.CENTER );

				button.mUI.setOnClickListener( new OnClickListener( )
				{
					public void onClick( View arg0 )
					{
						synchronized( FancyGLRenderer.render ) 
						{
							FancyMessage msg = new FancyMessage( );
							msg.mType = FancyMessage._EVENT_BUTTON_CLICK;
							msg.mWindow = button.mFancyUI;
							FancyGLRenderer.mMessages.add( msg );
						}
					}
				} );
				UIGlobal.layout.addView( button.mUI );

				( (AbsoluteLayout.LayoutParams) button.mUI.getLayoutParams( ) ).x = button.mX;
				( (AbsoluteLayout.LayoutParams) button.mUI.getLayoutParams( ) ).y = button.mY;
				button.mUI.getLayoutParams( ).width = button.mW;
				button.mUI.getLayoutParams( ).height = button.mH;
			}
			break;

			case UIGlobal.BUTTON_IMAGE:
			{
				final AndroidButton button = (AndroidButton) msg.obj;

				StateListDrawable bg = new StateListDrawable( );
				bg.addState( new int[]{ -android.R.attr.state_enabled }, button.mDisabledImage );
				bg.addState( new int[]{ android.R.attr.state_pressed }, button.mClickImage );
				bg.addState( new int[]{ }, button.mNormalImage );

				button.mUI.setBackgroundDrawable( bg );
			}
			break;

			case UIGlobal.BUTTON_REMOVE:
			{
				AndroidButton button = (AndroidButton) msg.obj;
				UIGlobal.layout.removeView( button.mUI );
			}
			break;

			case UIGlobal.BUTTON_TITLE:
			{
				AndroidButton button = (AndroidButton) msg.obj;
				( (Button) button.mUI ).setText( button.mText );
			}
			break;

			case UIGlobal.BUTTON_TITLE_COLOR:
			{
				AndroidButton button = (AndroidButton) msg.obj;
				( (Button) button.mUI ).setTextColor( button.mTitleColor );
			}
			break;

			case UIGlobal.BUTTON_TITLE_SIZE:
			{
				AndroidButton button = (AndroidButton) msg.obj;
				( (Button) button.mUI ).setTextSize( TypedValue.COMPLEX_UNIT_PX, button.mTitleSize );
			}
			break;

			case UIGlobal.BUTTON_BACKGROUND_COLOR:
			{
				AndroidButton button = (AndroidButton) msg.obj;
				button.mUI.setBackgroundColor( button.mBackColor );
			}
			break;

			case UIGlobal.LABEL:
			{
				final AndroidUI label = (AndroidUI) msg.obj;
				label.mUI = new TextView( UIGlobal.active );
				label.mUI.setVisibility( View.GONE );
				( (TextView) label.mUI ).setSingleLine( );
				( (TextView) label.mUI ).setGravity( Gravity.CENTER );

				//TODO.if no setOnClickListener,label would crash.
				label.mUI.setOnClickListener( new OnClickListener( )
				{
					public void onClick( View arg0 )
					{
						synchronized( FancyGLRenderer.render ) 
						{
							FancyMessage msg = new FancyMessage( );
							FancyGLRenderer.mMessages.add( msg );
						}
					}
				} );

				UIGlobal.layout.addView( label.mUI );

				( (AbsoluteLayout.LayoutParams) label.mUI.getLayoutParams( ) ).x = label.mX;
				( (AbsoluteLayout.LayoutParams) label.mUI.getLayoutParams( ) ).y = label.mY;
				label.mUI.getLayoutParams( ).width = label.mW;
				label.mUI.getLayoutParams( ).height = label.mH;
			}
			break;

			case UIGlobal.LABEL_TEXT:
			{
				AndroidLabel label = (AndroidLabel) msg.obj;
				( (TextView) label.mUI ).setText( label.mText );
			}
			break;

			case UIGlobal.LABEL_TEXT_COLOR:
			{
				AndroidLabel label = (AndroidLabel) msg.obj;
				( (TextView) label.mUI ).setTextColor( label.mTitleColor );
			}
			break;

			case UIGlobal.LABEL_TEXT_SIZE:
			{
				AndroidLabel label = (AndroidLabel) msg.obj;
				( (TextView) label.mUI ).setTextSize( TypedValue.COMPLEX_UNIT_PX, label.mTitleSize );
			}
			break;

			case UIGlobal.LABEL_BACKGROUND_COLOR:
			{
				AndroidLabel label = (AndroidLabel) msg.obj;
				label.mUI.setBackgroundColor( label.mBackColor );
			}
			break;
			
			case UIGlobal.SPIN:
			{
				final AndroidUI spin = (AndroidUI) msg.obj;
				spin.mUI = new ViewGroup( UIGlobal.active )
				{
					@Override
					protected void onLayout( boolean changed, int l, int t, int r, int b )
					{
						getChildAt(0).layout( 0, 0, getLayoutParams( ).width / 4, getLayoutParams( ).height );
						getChildAt(1).layout( getLayoutParams( ).width / 4, 0, getLayoutParams( ).width * 3 / 4, getLayoutParams( ).height );
						getChildAt(2).layout( getLayoutParams( ).width * 3 / 4, 0, getLayoutParams( ).width, getLayoutParams( ).height );
					}
				};
				spin.mUI.setVisibility( View.GONE );

				Button lbtn = new Button( UIGlobal.active );
				Button rbtn = new Button( UIGlobal.active );
				Button cbtn = new Button( UIGlobal.active );

				cbtn.setTextColor( Color.WHITE );
				cbtn.setTextSize( TypedValue.COMPLEX_UNIT_PX, 20 );
				cbtn.setGravity( Gravity.CENTER );

				lbtn.setOnClickListener( new OnClickListener( )
				{
					public void onClick( View arg0 )
					{
						synchronized( FancyGLRenderer.render )
						{
							FancyMessage msg = new FancyMessage( );
							msg.mType = FancyMessage._EVENT_SPIN_PCLICK;
							msg.mWindow = spin.mFancyUI;
							FancyGLRenderer.mMessages.add( msg );
						}
					}
				} );

				rbtn.setOnClickListener( new OnClickListener( )
				{
					public void onClick( View arg0 )
					{
						synchronized( FancyGLRenderer.render )
						{
							FancyMessage msg = new FancyMessage( );
							msg.mType = FancyMessage._EVENT_SPIN_NCLICK;
							msg.mWindow = spin.mFancyUI;
							FancyGLRenderer.mMessages.add( msg );
						}
					}
				} );

				( (ViewGroup) spin.mUI ).addView( lbtn, 0 );
				( (ViewGroup) spin.mUI ).addView( cbtn, 1 );
				( (ViewGroup) spin.mUI ).addView( rbtn, 2 );
				UIGlobal.layout.addView( spin.mUI );

				( (AbsoluteLayout.LayoutParams) spin.mUI.getLayoutParams( ) ).x = spin.mX;
				( (AbsoluteLayout.LayoutParams) spin.mUI.getLayoutParams( ) ).y = spin.mY;
				spin.mUI.getLayoutParams( ).width = spin.mW;
				spin.mUI.getLayoutParams( ).height = spin.mH;
			}
			break;

			case UIGlobal.SPIN_VALUE:
			{
				AndroidSpin spin = (AndroidSpin) msg.obj;
				( (Button) ( (ViewGroup) spin.mUI ).getChildAt(1) ).setText( spin.mText );
			}
			break;

			case UIGlobal.SPIN_IMAGE:
			{
				final AndroidSpin spin = (AndroidSpin) msg.obj;

				( (Button) ( (ViewGroup) spin.mUI ).getChildAt(1) ).setBackgroundDrawable( spin.mCenter );

				StateListDrawable preBg = new StateListDrawable( );
				preBg.addState( new int[]{ android.R.attr.state_pressed }, spin.mLeftDown );
				preBg.addState( new int[]{}, spin.mLeftUp );
				( (Button) ( (ViewGroup) spin.mUI ).getChildAt(0) ).setBackgroundDrawable( preBg );

				StateListDrawable nextBg = new StateListDrawable( );
				nextBg.addState( new int[]{ android.R.attr.state_pressed }, spin.mRightDown );
				nextBg.addState( new int[]{}, spin.mRightUp );
				( (Button) ( (ViewGroup) spin.mUI ).getChildAt(2) ).setBackgroundDrawable( nextBg );
			}
			break;

			case UIGlobal.SPIN_REMOVE:
			{
				final AndroidSpin spin = (AndroidSpin) msg.obj;
			}
			break;

			case UIGlobal.EDIT:
			{
				final AndroidUI textInput = (AndroidUI) msg.obj;
				textInput.mUI = new EditText( UIGlobal.active );
				textInput.mUI.setVisibility( View.GONE );
				((EditText) textInput.mUI).setSingleLine( true );
				((EditText) textInput.mUI).setGravity( Gravity.CENTER );
				((EditText) textInput.mUI).setEllipsize( TextUtils.TruncateAt.valueOf( "END" ) );

				((EditText) textInput.mUI).addTextChangedListener( new TextWatcher( ) 
				{
					@Override
					public void beforeTextChanged( CharSequence s, int start, int count, int after ) 
					{
					}

					@Override
					public void onTextChanged(CharSequence arg0, int arg1, int arg2, int arg3)
					{
					}
					
					@Override
					public void afterTextChanged( Editable s )
					{
						//TODO. Thread safe.
						textInput.mText = s.toString( );
						synchronized( FancyGLRenderer.render )
						{
							FancyMessage msg = new FancyMessage( );
							msg.mType = FancyMessage._EVENT_EDIT_CHANGE;
							msg.mWindow = textInput.mFancyUI;
							msg.mIsArea = false;
							FancyGLRenderer.mMessages.add( msg );
						}
					}
				});

				UIGlobal.layout.addView( textInput.mUI );

				( (AbsoluteLayout.LayoutParams) textInput.mUI.getLayoutParams( ) ).x = textInput.mX;
				( (AbsoluteLayout.LayoutParams) textInput.mUI.getLayoutParams( ) ).y = textInput.mY;
				textInput.mUI.getLayoutParams( ).width = textInput.mW;
				textInput.mUI.getLayoutParams( ).height = textInput.mH;
			}
			break;

			case UIGlobal.EDIT_SET_TEXT:
			{
				AndroidTextInput textInput = (AndroidTextInput) msg.obj;
				( (EditText) textInput.mUI ).setText( textInput.mText );
			}
			break;

			case UIGlobal.EDIT_SET_TEXTSIZE:
			{
				AndroidTextInput textInput = (AndroidTextInput) msg.obj;
				( (EditText) textInput.mUI ).setTextSize( TypedValue.COMPLEX_UNIT_PX, textInput.mTextSize );
			}
			break;

			case UIGlobal.EDIT_SET_TEXTCOLOR:
			{
				AndroidTextInput textInput = (AndroidTextInput) msg.obj;
				( (EditText) textInput.mUI ).setTextColor( textInput.mTextColor );
			}
			break;

			case UIGlobal.EDIT_PASSWORD:
			{
				AndroidTextInput textInput = (AndroidTextInput) msg.obj;
				if ( textInput.mIsSecure )
					( (EditText) textInput.mUI ).setInputType( InputType.TYPE_CLASS_TEXT | InputType.TYPE_TEXT_VARIATION_PASSWORD );
				else
					( (EditText) textInput.mUI ).setInputType( InputType.TYPE_CLASS_TEXT | InputType.TYPE_TEXT_VARIATION_VISIBLE_PASSWORD );
			}
			break;

			case UIGlobal.EDIT_IMAGE:
			{
				AndroidTextInput textInput = (AndroidTextInput) msg.obj;
				textInput.mUI.setBackgroundDrawable( textInput.mImage );
			}
			break;

			case UIGlobal.EDIT_REMOVE:
			{
				AndroidTextInput textInput = (AndroidTextInput) msg.obj;
				UIGlobal.layout.removeView( textInput.mUI );
			}
			break;
			
			case UIGlobal.CHECKBOX:
			{
				final AndroidUI cBox = (AndroidUI) msg.obj;
				cBox.mUI = new Button( UIGlobal.active );
				cBox.mUI.setVisibility( View.GONE );

				( (Button) cBox.mUI ).setOnClickListener( new OnClickListener( )
				{
					@Override
					public void onClick( View arg0 )
					{
						synchronized( FancyGLRenderer.render )
						{
							arg0.setSelected( !arg0.isSelected( ) );
							FancyMessage msg = new FancyMessage( );
							msg.mType = FancyMessage._EVENT_CHECK_SELECT;
							msg.mWindow = cBox.mFancyUI;
							msg.mIsSelect = arg0.isSelected( );
							FancyGLRenderer.mMessages.add( msg );
						}
					}
				} );

				UIGlobal.layout.addView( cBox.mUI );

				( (AbsoluteLayout.LayoutParams) cBox.mUI.getLayoutParams( ) ).x = cBox.mX;
				( (AbsoluteLayout.LayoutParams) cBox.mUI.getLayoutParams( ) ).y = cBox.mY;
				cBox.mUI.getLayoutParams( ).width = cBox.mW;
				cBox.mUI.getLayoutParams( ).height = cBox.mH;
			}
			break;

			case UIGlobal.CHECKBOX_IMAGE:
			{
				AndroidCheckBox cBox = (AndroidCheckBox) msg.obj;

				StateListDrawable sl = new StateListDrawable( );
				sl.addState( new int[]{ android.R.attr.state_selected }, cBox.mSelect );
				sl.addState( new int[]{}, cBox.mNormal );
				cBox.mUI.setBackgroundDrawable( sl );
			}
			break;

			case UIGlobal.CHECKBOX_REMOVE:
			{
				AndroidCheckBox cBox = (AndroidCheckBox) msg.obj;
				UIGlobal.layout.removeView( cBox.mUI );
			}
			break;

			case UIGlobal.PANEL:
			{
				final AndroidUI image = (AndroidUI) msg.obj;
				image.mUI = new ImageView( UIGlobal.active );
				image.mUI.setVisibility( View.GONE );

				image.mUI.setOnClickListener( new OnClickListener( )
				{
					public void onClick( View arg0 )
					{
						synchronized( FancyGLRenderer.render ) 
						{
							FancyMessage msg = new FancyMessage( );
							FancyGLRenderer.mMessages.add( msg );
						}
					}
				} );

				UIGlobal.layout.addView( image.mUI );

				( (AbsoluteLayout.LayoutParams) image.mUI.getLayoutParams( ) ).x = image.mX;
				( (AbsoluteLayout.LayoutParams) image.mUI.getLayoutParams( ) ).y = image.mY;
				image.mUI.getLayoutParams().width = UIGlobal.active.getWindowManager( ).getDefaultDisplay( ).getWidth( );
				image.mUI.getLayoutParams().height =  UIGlobal.active.getWindowManager( ).getDefaultDisplay( ).getHeight( );
				( (ImageView) image.mUI ).setScaleType( ScaleType.FIT_XY );
			}
			break;
			
			case UIGlobal.PANEL_IMAGE:
			{
				AndroidPanel image = (AndroidPanel) msg.obj;
				( (ImageView) image.mUI ).setImageBitmap( image.mImage.getBitmap( ) );
			}
			break;

			case UIGlobal.PANEL_REMOVE:
			{
				AndroidPanel image = (AndroidPanel) msg.obj;
				UIGlobal.layout.removeView( image.mUI );
			}
			break;

			case UIGlobal.TILELIST:
			{
				final AndroidUI tilelist = (AndroidUI) msg.obj;
				tilelist.mUI = new ListView( UIGlobal.active );
				tilelist.mUI.setVisibility( View.GONE );
				tilelist.mAdapter = new ArrayAdapter<String>( UIGlobal.active, android.R.layout.simple_expandable_list_item_1, tilelist.mData );
				( (ListView) tilelist.mUI ).setAdapter( tilelist.mAdapter );

				( (ListView) tilelist.mUI ).setOnItemClickListener( new OnItemClickListener( )
				{
					@Override
					public void onItemClick(AdapterView<?> arg0, View arg1, int arg2, long arg3) 
					{
						tilelist.mIndex = (int) arg3;
						synchronized( FancyGLRenderer.render )
						{
							FancyMessage msg = new FancyMessage( );
							msg.mType = FancyMessage._EVENT_TILELIST_CLICK;
							msg.mWindow = tilelist.mFancyUI;
							FancyGLRenderer.mMessages.add( msg );
						}
					}
				});

				UIGlobal.layout.addView( tilelist.mUI );

				( (AbsoluteLayout.LayoutParams) tilelist.mUI.getLayoutParams( ) ).x = tilelist.mX;
				( (AbsoluteLayout.LayoutParams) tilelist.mUI.getLayoutParams( ) ).y = tilelist.mY;
				tilelist.mUI.getLayoutParams( ).width = tilelist.mW;
				tilelist.mUI.getLayoutParams( ).height = tilelist.mH;
			}
			break;

			case UIGlobal.TILELIST_TEXT_SIZE:
			{
				AndroidTileList tileList = (AndroidTileList) msg.obj;
				//TODO
			}
			break;

			case UIGlobal.TILELIST_PUSH:
			{
				AndroidTileList tileList = (AndroidTileList) msg.obj;
				tileList.mAdapter.notifyDataSetChanged( );
			}
			break;

			case UIGlobal.TILELIST_CLEANUP:
			{
				AndroidTileList tileList = (AndroidTileList) msg.obj;
				tileList.mAdapter.notifyDataSetChanged( );
			}
			break;

			case UIGlobal.TILELIST_INVALIDDATE:
			{
				AndroidTileList tileList = (AndroidTileList) msg.obj;
				tileList.mUI.invalidate( );
			}
			break;

			case UIGlobal.TEXTAREA:
			{
				final AndroidUI textArea = (AndroidUI) msg.obj;
				textArea.mUI = new EditText( UIGlobal.active );
				textArea.mUI.setVisibility( View.GONE );
				textArea.mUI.setEnabled( false );

				//TODO.if no setOnClickListener,textArea would crash.
				textArea.mUI.setOnClickListener( new OnClickListener( )
				{
					public void onClick( View arg0 )
					{
						synchronized( FancyGLRenderer.render ) 
						{
							FancyMessage msg = new FancyMessage( );
							FancyGLRenderer.mMessages.add( msg );
						}
					}
				} );

				UIGlobal.layout.addView( textArea.mUI );

				( (AbsoluteLayout.LayoutParams) textArea.mUI.getLayoutParams( ) ).x = textArea.mX;
				( (AbsoluteLayout.LayoutParams) textArea.mUI.getLayoutParams( ) ).y = textArea.mY;
				textArea.mUI.getLayoutParams( ).width = textArea.mW;
				textArea.mUI.getLayoutParams( ).height = textArea.mH;
			}
			break;

			case UIGlobal.TEXTAREA_EDITABLE:
			{
				final AndroidTextArea textArea = (AndroidTextArea) msg.obj;
				( (EditText) textArea.mUI ).setEnabled( textArea.mIsEditable );

				((EditText) textArea.mUI).addTextChangedListener( new TextWatcher( ) 
				{
					@Override
					public void beforeTextChanged( CharSequence s, int start, int count, int after ) 
					{
					}

					@Override
					public void onTextChanged(CharSequence arg0, int arg1, int arg2, int arg3)
					{
					}

					@Override
					public void afterTextChanged( Editable s )
					{
						//TODO. Thread safe.
						textArea.mText = s.toString( );
						synchronized( FancyGLRenderer.render )
						{
							FancyMessage msg = new FancyMessage( );
							msg.mType = FancyMessage._EVENT_EDIT_CHANGE;
							msg.mWindow = textArea.mFancyUI;
							msg.mIsArea = true;
							FancyGLRenderer.mMessages.add( msg );
						}
					}
				});
			}

			case UIGlobal.TEXTAREA_TEXT:
			{
				AndroidTextArea textArea = (AndroidTextArea) msg.obj;
				( (EditText) textArea.mUI ).setText( textArea.mText );
			}
			break;

			case UIGlobal.TEXTAREA_IMAGE:
			{
				AndroidTextArea textArea = (AndroidTextArea) msg.obj;
				textArea.mUI.setBackgroundDrawable( textArea.mImage );
			}
			break;

			case UIGlobal.TEXTAREA_TEXTSIZE:
			{
				AndroidTextArea textArea = (AndroidTextArea) msg.obj;
				( (EditText) textArea.mUI ).setTextSize( TypedValue.COMPLEX_UNIT_PX, textArea.mSize );
			}
			break;

			case UIGlobal.TEXTAREA_TEXTCOLOR:
			{
				AndroidTextArea textArea = (AndroidTextArea) msg.obj;
				( (EditText) textArea.mUI ).setTextColor( textArea.mTextColor );
			}
			break;

			case UIGlobal.TEXTAREA_ALIGN:
			{
				AndroidTextArea textArea = (AndroidTextArea) msg.obj;
				if ( textArea.mAlign == 0x00 )
					( (EditText) textArea.mUI ).setGravity( Gravity.LEFT );
				else if ( textArea.mAlign == 0x01 )
					( (EditText) textArea.mUI ).setGravity( Gravity.CENTER_HORIZONTAL );
				else if ( textArea.mAlign == 0x02 )
					( (EditText) textArea.mUI ).setGravity( Gravity.RIGHT );
				else if ( textArea.mAlign == 0x10 )
					( (EditText) textArea.mUI ).setGravity( Gravity.CENTER_VERTICAL );
				else if ( textArea.mAlign == 0x11 )
					( (EditText) textArea.mUI ).setGravity( Gravity.CENTER );
				else if ( textArea.mAlign == 0x12 )
					( (EditText) textArea.mUI ).setGravity( Gravity.RIGHT | Gravity.CENTER );
				else if ( textArea.mAlign == 0x20 )
					( (EditText) textArea.mUI ).setGravity( Gravity.BOTTOM );
				else if ( textArea.mAlign == 0x21 )
					( (EditText) textArea.mUI ).setGravity( Gravity.BOTTOM | Gravity.CENTER );
				else if ( textArea.mAlign == 0x22 )
					( (EditText) textArea.mUI ).setGravity( Gravity.BOTTOM | Gravity.RIGHT );
			}
			break;

			case UIGlobal.TEXTAREA_REMOVE:
			{
				AndroidTextArea textArea = (AndroidTextArea) msg.obj;
				UIGlobal.layout.removeView( textArea.mUI );
			}
			break;

			case UIGlobal.VIDEO:
			{
				final AndroidVideo video = (AndroidVideo) msg.obj;
				video.createMediaPlayer( );
			}
			break;
			
			case UIGlobal.VIDEO_PLAY:
			{
				final AndroidVideo video = (AndroidVideo) msg.obj;
				UIGlobal.glView.setVisibility( View.GONE );
				UIGlobal.videoview.setVisibility( View.VISIBLE );
				if ( video.mFill == false )
				{
					int width = FancyJni.getDeviceWidth( ), height = FancyJni.getDeviceHeight( ), videoWidth = video.mMediaPlayer.getVideoWidth( ), videoHeight = video.mMediaPlayer.getVideoHeight( );
					if ( videoWidth * height > width * videoHeight )
						height = width * videoHeight / videoWidth;
					else if ( videoWidth * height < width * videoHeight )
						width = height * videoWidth / videoHeight;

					UIGlobal.videoview.setX( ( FancyJni.getDeviceWidth( ) - width ) / 2 );
					UIGlobal.videoview.setY( ( FancyJni.getDeviceHeight( ) - height ) / 2 );
					UIGlobal.videoview.getHolder( ).setFixedSize( width, height );
				}

				video.mMediaPlayer.start( );
				if ( video.getDone( ) )
					video.mMediaPlayer.seekTo(0);
				video.setDone(false);
			}
			break;

			case UIGlobal.VIDEO_PAUSE:
			{
				final AndroidVideo video = (AndroidVideo) msg.obj;
				video.mMediaPlayer.pause( );
			}
			break;

			case UIGlobal.VIDEO_STOP:
			{
				final AndroidVideo video = (AndroidVideo) msg.obj;
				UIGlobal.glView.setVisibility( View.VISIBLE );
				UIGlobal.videoview.setVisibility( View.GONE );
				video.mMediaPlayer.stop( );
				video.setDone(true);
			}
			break;

			case UIGlobal.VIDEO_RELEASE:
			{
				final AndroidVideo video = (AndroidVideo) msg.obj;
				video.mMediaPlayer.stop( );
				video.mMediaPlayer.release( );
				video.mMediaPlayer = null;
			}
			break;

			case UIGlobal.GFX_EDIT:
			{
				UIGlobal.inputView = new EditText( UIGlobal.active );
				UIGlobal.gfx_edit = new AlertDialog.Builder( UIGlobal.active )
									.setTitle( "Please Input" )
									.setView( UIGlobal.inputView )
									.setPositiveButton( "Done", new DialogInterface.OnClickListener( )
									{
										public void onClick( DialogInterface dialog, int whichButton )
										{
											for ( int i = 0; i < UIGlobal.text.length( ); i ++ )
											{
												synchronized ( FancyGLRenderer.render )
												{
													FancyMessage msg = new FancyMessage( );
													msg.mType = FancyMessage._EVENT_GFXEDIT_CHANGE;
													msg.mKey = BACKSPACE;
													FancyGLRenderer.mMessages.add( msg );
												}
											}

											for ( int i = 0; i < UIGlobal.inputView.getText( ).length( ); i ++ )
											{
												synchronized( FancyGLRenderer.render )
												{
													FancyMessage msg = new FancyMessage( );
													msg.mType = FancyMessage._EVENT_GFXEDIT_CHANGE;
													msg.mKey = UIGlobal.inputView.getText( ).toString( ).toCharArray( )[i];
													FancyGLRenderer.mMessages.add( msg );
												}
											}

											synchronized( FancyGLRenderer.render )
											{
												FancyMessage msg = new FancyMessage( );
												msg.mType = FancyMessage._EVENT_GFXEDIT_CHANGE;
												msg.mKey = LOSEFOCUS;
												FancyGLRenderer.mMessages.add( msg );
											}
										}
									} )
									.setNegativeButton( "Cancel", new DialogInterface.OnClickListener( )
									{
										public void onClick( DialogInterface dialog, int whichButton )
										{
											synchronized( FancyGLRenderer.render )
											{
												FancyMessage msg = new FancyMessage( );
												msg.mType = FancyMessage._EVENT_GFXEDIT_CHANGE;
												msg.mKey = LOSEFOCUS;
												FancyGLRenderer.mMessages.add( msg );
											}
										}
									})
									.create( );
			}
			break;

			case UIGlobal.GFX_GET_FOCUS:
			{
				UIGlobal.glLayout.getViewTreeObserver( ).removeGlobalOnLayoutListener( UIGlobal.globalLayoutListener );

				if ( UIGlobal.password )
					UIGlobal.inputView.setInputType( InputType.TYPE_CLASS_TEXT | InputType.TYPE_TEXT_VARIATION_PASSWORD );
				else
					UIGlobal.inputView.setInputType( InputType.TYPE_TEXT_VARIATION_VISIBLE_PASSWORD );

				UIGlobal.inputView.setText( UIGlobal.text );
				UIGlobal.inputView.setSelection( UIGlobal.text.length( ) );

				UIGlobal.gfx_edit.show( );
				UIGlobal.gfx_edit.setTitle( UIGlobal.inputViewTitle.isEmpty( ) ? "Please Input" : UIGlobal.inputViewTitle );
				UIGlobal.gfx_edit.getButton( AlertDialog.BUTTON_NEGATIVE ).setText( UIGlobal.inputViewCancelBar.isEmpty( ) ? "Cancel" : UIGlobal.inputViewCancelBar );
				UIGlobal.gfx_edit.getButton( AlertDialog.BUTTON_POSITIVE ).setText( UIGlobal.inputViewDoneBar.isEmpty( ) ? "Done" : UIGlobal.inputViewDoneBar );
			}
			break;

			case UIGlobal.LUA_UI_INIT_EDIT:
			{
				UIGlobal.LUA_UI_INPUT_HEIGHT = FancyJni.GetDensityDpi( ) / 3;
				UIGlobal.LUA_UI_DONE_WIDTH = UIGlobal.LUA_UI_INPUT_HEIGHT * 4 / 3;

				UIGlobal.relativeLayout = new RelativeLayout( UIGlobal.active );
				UIGlobal.glLayout.addView( UIGlobal.relativeLayout );
				UIGlobal.relativeLayout.setVisibility( View.INVISIBLE );
				( (AbsoluteLayout.LayoutParams) UIGlobal.relativeLayout.getLayoutParams( ) ).x = 0;
				( (AbsoluteLayout.LayoutParams) UIGlobal.relativeLayout.getLayoutParams( ) ).y = 0;
				UIGlobal.relativeLayout.getLayoutParams( ).width = UIGlobal.active.getWindowManager( ).getDefaultDisplay( ).getWidth( );
				UIGlobal.relativeLayout.getLayoutParams( ).height = UIGlobal.LUA_UI_INPUT_HEIGHT;

				UIGlobal.uiInput = new EditText( UIGlobal.active );
				UIGlobal.uiInput.setSingleLine( );
				UIGlobal.uiInput.setId( 1 ); 
				UIGlobal.textWatcher = new TextWatcher( )
				{
					@Override
					public void onTextChanged( CharSequence s, int start, int before, int count ) { }
					
					@Override
					public void beforeTextChanged( CharSequence s, int start, int count, int after ) { }
					
					@Override
					public void afterTextChanged( Editable s )
					{
						synchronized( FancyGLRenderer.render )
						{
							FancyMessage msg = new FancyMessage( );
							msg.mType = FancyMessage._EVENT_KEYBOARD;
							msg.mStr = s.toString( );
							FancyGLRenderer.mMessages.add( msg );
						}
					}
				};

				UIGlobal.uiInput.setOnEditorActionListener( new OnEditorActionListener( )
				{
					@Override
					public boolean onEditorAction( TextView v, int actionId, KeyEvent event )
					{
						if ( actionId == EditorInfo.IME_ACTION_DONE || actionId == EditorInfo.IME_ACTION_NEXT || actionId == EditorInfo.IME_ACTION_GO )
						{
							synchronized( FancyGLRenderer.render )
							{
								FancyMessage msg = new FancyMessage( );
								msg.mType = FancyMessage._EVENT_GFXEDIT_CHANGE;
								msg.mKey = LOSEFOCUS;
								FancyGLRenderer.mMessages.add( msg );
							}

							UIGlobal.uiInput.removeTextChangedListener( UIGlobal.textWatcher );
							UIGlobal.uiInput.setText( "" );
							( (InputMethodManager) UIGlobal.active.getSystemService( Context.INPUT_METHOD_SERVICE ) ).hideSoftInputFromWindow( UIGlobal.uiInput.getWindowToken( ), InputMethodManager.HIDE_NOT_ALWAYS );
							UIGlobal.relativeLayout.setVisibility( View.INVISIBLE );

							return true;
						}

						return false;
					}
				});

				RelativeLayout.LayoutParams lp1 = new RelativeLayout.LayoutParams( UIGlobal.active.getWindowManager( ).getDefaultDisplay( ).getWidth( ) - UIGlobal.LUA_UI_DONE_WIDTH, ViewGroup.LayoutParams.MATCH_PARENT );
				lp1.addRule( RelativeLayout.ALIGN_PARENT_LEFT );
				UIGlobal.relativeLayout.addView( UIGlobal.uiInput, lp1 );

				UIGlobal.btnDone = new Button( UIGlobal.active );
				UIGlobal.btnDone.setText( "Done" );
				UIGlobal.btnDone.setOnClickListener( new OnClickListener( )
				{
					@Override
					public void onClick( View v )
					{
						if ( UIGlobal.uiInput == null )
							return;

						synchronized( FancyGLRenderer.render )
						{
							FancyMessage msg = new FancyMessage( );
							msg.mType = FancyMessage._EVENT_GFXEDIT_CHANGE;
							msg.mKey = LOSEFOCUS;
							FancyGLRenderer.mMessages.add( msg );
						}

						UIGlobal.uiInput.removeTextChangedListener( UIGlobal.textWatcher );
						UIGlobal.uiInput.setText( "" );
						( (InputMethodManager) UIGlobal.active.getSystemService( Context.INPUT_METHOD_SERVICE ) ).hideSoftInputFromWindow( UIGlobal.glLayout.getWindowToken( ), 0 );
						UIGlobal.relativeLayout.setVisibility( View.INVISIBLE );
					}
				});

				RelativeLayout.LayoutParams lp2 = new RelativeLayout.LayoutParams( UIGlobal.LUA_UI_DONE_WIDTH, ViewGroup.LayoutParams.MATCH_PARENT );
				lp2.addRule( RelativeLayout.RIGHT_OF, UIGlobal.uiInput.getId( ) );
				UIGlobal.relativeLayout.addView( UIGlobal.btnDone, lp2 );

				UIGlobal.globalLayoutListener = new ViewTreeObserver.OnGlobalLayoutListener( )
				{
					@Override
					public void onGlobalLayout( ) 
					{
						Rect rect = new Rect( );
						UIGlobal.glLayout.getWindowVisibleDisplayFrame( rect );

						if ( UIGlobal.keyboardHeight != UIGlobal.glLayout.getRootView( ).getHeight( ) - ( rect.bottom - rect.top ) )
						{
							UIGlobal.keyboardHeight = UIGlobal.glLayout.getRootView( ).getHeight( ) - ( rect.bottom - rect.top );

							synchronized ( FancyGLRenderer.render )
							{
								FancyMessage msg = new FancyMessage( );
								if ( UIGlobal.keyboardHeight == 0 )
								{
									msg.mType = FancyMessage._EVENT_RESTORE_TEXTBOX;
								}
								else
								{
									msg.mType = FancyMessage._EVENT_VISIBLE_TEXTBOX;
									msg.mKeyboardHeight = UIGlobal.keyboardHeight;
									msg.mX1 = UIGlobal.x1;
									msg.mY1 = UIGlobal.y1;
									msg.mX2 = UIGlobal.x2;
									msg.mY2 = UIGlobal.y2;
								}
	
								FancyGLRenderer.mMessages.add( msg );
							}
						}
					}
				};
			}
			break;

			case UIGlobal.LUA_UI_SHOW_EDIT:
			{
				UIGlobal.uiInput.setText( UIGlobal.text );
				UIGlobal.uiInput.setSelection( UIGlobal.text.length( ) );
				UIGlobal.relativeLayout.setVisibility( View.VISIBLE );

				UIGlobal.glLayout.getViewTreeObserver( ).removeGlobalOnLayoutListener( UIGlobal.globalLayoutListener );
				UIGlobal.glLayout.getViewTreeObserver( ).addOnGlobalLayoutListener( UIGlobal.globalLayoutListener );

				InputMethodManager imm = (InputMethodManager) UIGlobal.active.getSystemService( Context.INPUT_METHOD_SERVICE );
				UIGlobal.uiInput.requestFocus( );
				imm.showSoftInput( UIGlobal.uiInput, 0 );

				UIGlobal.uiInput.removeTextChangedListener( UIGlobal.textWatcher );
				UIGlobal.uiInput.addTextChangedListener( UIGlobal.textWatcher );
			}
			break;

			case UIGlobal.LUA_UI_HIDE_EDIT:
			{
				if ( UIGlobal.uiInput == null )
					return;

				UIGlobal.uiInput.removeTextChangedListener( UIGlobal.textWatcher );
				UIGlobal.uiInput.setText( "" );
				( (InputMethodManager) UIGlobal.active.getSystemService( Context.INPUT_METHOD_SERVICE ) ).hideSoftInputFromWindow( UIGlobal.uiInput.getWindowToken( ), InputMethodManager.HIDE_NOT_ALWAYS );
				UIGlobal.relativeLayout.setVisibility( View.INVISIBLE );
			}
			break;

			case UIGlobal.LUA_UI_REMOVE_EDIT:
			{
				UIGlobal.relativeLayout.removeAllViews( );
				UIGlobal.glLayout.removeView( UIGlobal.relativeLayout );
			}
			break;

			case UIGlobal.PROMPT:
			{
				Hashtable<String, String> ht = (Hashtable<String, String>) msg.obj;
				int type = Integer.parseInt( ht.get("type") );
				AlertDialog alert = new AlertDialog.Builder( UIGlobal.active )
				.setTitle( ht.get("title") )
				.setMessage( ht.get("context") )
				.create( );

				Message message = null;
				switch ( type )
				{
					case 0:
					{
						alert.setButton( DialogInterface.BUTTON_POSITIVE, "确定", message );
					}
					break;

					case 1:
					{
						alert.setButton( DialogInterface.BUTTON_POSITIVE, "确定", message );
						alert.setButton( DialogInterface.BUTTON_NEGATIVE, "取消", message );
					}
					break;
				}

				alert.show( );
			}
			break;
		}
	}
}