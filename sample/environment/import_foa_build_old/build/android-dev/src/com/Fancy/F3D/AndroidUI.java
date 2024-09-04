package com.Fancy.F3D;

import java.util.ArrayList;
import android.view.View;
import android.widget.ArrayAdapter;

import com.Fancy.Application.UIGlobal;

public class AndroidUI
{
	public View					mUI;
	public int					mFancyUI;
	public int					mX;
	public int					mY;
	public int					mW;
	public int					mH;
	public int					mIndex;
	public String				mText;
	public boolean				mIsEnable;
	public boolean				mIsShow;
	public ArrayList<String>	mData;
	public ArrayAdapter<String>	mAdapter;

	public void CreateAndroidButton( int fancy , int x, int y, int width, int height )
	{
		mFancyUI = fancy;
		mX = x;
		mY = y;
		mW = width;
		mH = height;

		UIGlobal.sendMessage( this, UIGlobal.BUTTON );
	}
	
	public void CreateAndroidLabel( int fancy , int x, int y, int width, int height )
	{
		mFancyUI = fancy;
		mX = x;
		mY = y;
		mW = width;
		mH = height;

		UIGlobal.sendMessage( this, UIGlobal.LABEL );
	}
	
	public void CreateAndroidCheckBox( int fancy, int x, int y, int width, int height )
	{
		mFancyUI = fancy;
		mX = x;
		mY = y;
		mW = width;
		mH = height;

		UIGlobal.sendMessage( this, UIGlobal.CHECKBOX );
	}
	
	public void CreateAndroidTextInput( int fancy, int x, int y, int width, int height )
	{
		mFancyUI = fancy;
		mX = x;
		mY = y;
		mW = width;
		mH = height;

		UIGlobal.sendMessage( this, UIGlobal.EDIT );
	}

	public void CreateAndroidTileList( int fancy, int x, int y, int width, int height )
	{
		mFancyUI = fancy;
		mX = x;
		mY = y;
		mW = width;
		mH = height;
		mData = new ArrayList<String>( );

		UIGlobal.sendMessage( this, UIGlobal.TILELIST );
	}

	public void CreateAndroidPanel( int fancy, int x, int y, int width, int height )
	{
		mFancyUI = fancy;
		mX = x;
		mY = y;
		mW = width;
		mH = height;

		UIGlobal.sendMessage( this, UIGlobal.PANEL );
	}

	public void CreateAndroidSpin( int fancy, int x, int y, int width, int height )
	{
		mFancyUI = fancy;
		mX = x;
		mY = y;
		mW = width;
		mH = height;

		UIGlobal.sendMessage( this, UIGlobal.SPIN );
	}

	public void CreateAndroidTextArea( int fancy, int x, int y, int width, int height )
	{
		mFancyUI = fancy;
		mX = x;
		mY = y;
		mW = width;
		mH = height;

		UIGlobal.sendMessage( this, UIGlobal.TEXTAREA );
	}

	public void setX( int x )
	{
		mX = x;
		UIGlobal.sendMessage( this, UIGlobal.SET_X );
	}

	public void setY( int y )
	{
		mY = y;
		UIGlobal.sendMessage( this, UIGlobal.SET_Y );
	}

	public void setW( int width )
	{
		mW = width;
		UIGlobal.sendMessage( this, UIGlobal.SET_W );
	}

	public void setH( int height )
	{
		mH = height;
		UIGlobal.sendMessage( this, UIGlobal.SET_H );
	}

	public void setEnable( boolean enable )
	{
		mIsEnable = enable;
		UIGlobal.sendMessage( this, UIGlobal.SET_ENABLE );
	}

	public void setShow( boolean show )
	{
		mIsShow = show;
		UIGlobal.sendMessage( this, UIGlobal.SET_SHOW );
	}
	
	public void setTop( )
	{
		UIGlobal.sendMessage( this, UIGlobal.SET_TOP );
	}

}
