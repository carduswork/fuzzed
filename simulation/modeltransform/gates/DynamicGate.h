#pragma once
#include "Gate.h"
#include <assert.h>

class DynamicGate : public Gate
{
public:
	DynamicGate(const std::string& ID, const std::string& name) : Gate(ID, name)
	{
		m_bDynamic = true;
		m_bStaticSubTree = false;
	}

	virtual std::string serializeAsFormula(boost::shared_ptr<PNDocument> doc) const override
	{
		return "DYNAMIC_BEHAVIOUR";
	}

	virtual int serializeTimeNet(boost::shared_ptr<TNDocument> doc) const override = 0;
};
