#include "ORGate.h"
#include "serialization/PNDocument.h"
#include "FaultTreeNode.h"

#include <iostream>

ORGate::ORGate(int id, const string& name /*= ""*/) 
	: Gate(id, name)
{
	m_bDynamic = false;

	m_activationFunc = [](NodeValueMap childValues) -> long double 
	{
		long double result = 1.0;
		for (const auto& p : childValues)
			result *= 1.0 - p.second;

		return 1.0L - result;
	};
}

ORGate::~ORGate(void)
{
}

int ORGate::serialize(boost::shared_ptr<PNDocument> doc) const 
{
	vector<int> childIDs;
	for (auto it = getChildrenBegin(); it != getChildrenEnd(); ++it)
		childIDs.push_back((*it)->serialize(doc));

	int placeID = doc->addPlace(0, 100, "OR_Failed");
	for (int id : childIDs)
	{
		if (id < 0)
		{
			cout << "Invalid child found, ID: " << id << endl;
			continue;
		}
		int transitionID = doc->addImmediateTransition();
		
		doc->placeToTransition(id, transitionID);
		doc->transitionToPlace(transitionID, placeID);
	}

	cout << "Value of OR: " << getValue() << endl;

	return placeID;
}

FaultTreeNode* ORGate::clone() const
{
	FaultTreeNode* newNode = new ORGate(m_id, m_name);
	for (auto& child : m_children)
	{
		newNode->addChild(child->clone());
	}
	return newNode;
}