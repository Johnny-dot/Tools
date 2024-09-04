package com.Fancy.F3D;

import com.Fancy.Application.UIGlobal;

import android.graphics.Color;

public class AndroidLabel extends AndroidUI
{
	public int		mTitleSize;
	public int		mTitleColor;
	public int		mBackColor;

	public void setText( String text )
	{
		mText = text;
		UIGlobal.sendMessage( this, UIGlobal.LABEL_TEXT );
	}

	public void setTextColor( int color )
	{
		mTitleColor = Color.rgb( ( color & 0xFF0000 ) >> 16, ( color & 0xFF00 ) >> 8, color & 0xFF );
		UIGlobal.sendMessage( this, UIGlobal.LABEL_TEXT_COLOR );
	}

	public void setTextSize( int size )
	{
		mTitleSize = size;
		UIGlobal.sendMessage( this, UIGlobal.LABEL_TEXT_SIZE );
	}
	
	public void setBgColor( int color )
	{
		mBackColor = Color.rgb( ( color & 0xFF0000 ) >> 16, ( color & 0xFF00 ) >> 8, color & 0xFF );
		UIGlobal.sendMessage( this, UIGlobal.LABEL_BACKGROUND_COLOR );
	}
}
