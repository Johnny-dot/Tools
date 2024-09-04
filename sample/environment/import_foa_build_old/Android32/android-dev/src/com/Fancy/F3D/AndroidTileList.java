package com.Fancy.F3D;

import com.Fancy.Application.UIGlobal;

public class AndroidTileList extends AndroidUI
{
	public int mTitleSize;

	public void setTextSize( int size )
	{
		mTitleSize = size;
		UIGlobal.sendMessage( this, UIGlobal.TILELIST_TEXT_SIZE );
	}
	
	public int getSelectedIndex( )
	{
		return mIndex;
	}
	
	public void push( String context )
	{
		mData.add( context );
		UIGlobal.sendMessage( this, UIGlobal.TILELIST_PUSH );
	}
	
	public void cleanUp( )
	{
		mData.clear( );
		UIGlobal.sendMessage( this, UIGlobal.TILELIST_CLEANUP );
	}
	
	public void invalidateData( )
	{
		UIGlobal.sendMessage( this, UIGlobal.TILELIST_INVALIDDATE );
	}
}
